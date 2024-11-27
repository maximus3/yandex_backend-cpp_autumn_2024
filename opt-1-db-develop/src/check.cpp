#include "check.hpp"

#include <fmt/format.h>

#include <exception>
#include <memory>
#include <string>
#include <userver/clients/dns/component.hpp>
#include <userver/components/component.hpp>
#include <userver/error_injection/settings_fwd.hpp>
#include <userver/formats/common/type.hpp>
#include <userver/formats/json/value_builder.hpp>
#include <userver/formats/serialize/common_containers.hpp>
#include <userver/logging/log.hpp>
#include <userver/server/handlers/http_handler_base.hpp>
#include <userver/server/http/http_response.hpp>
#include <userver/server/http/http_status.hpp>
#include <userver/storages/postgres/cluster.hpp>
#include <userver/storages/postgres/component.hpp>
#include <userver/utils/assert.hpp>
#include <utility>
#include "models/common_user.hpp"
#include "models/errors.hpp"
#include "models/product.hpp"

namespace code_architecture {

namespace {

std::pair<std::string, int> parceProductId(const std::string& item_id) {
  size_t underscore_pos = item_id.find('_');
  std::string type = item_id.substr(0, underscore_pos);
  std::string id_str = item_id.substr(underscore_pos + 1);

  int id = std::stoi(id_str);
  return std::make_pair(type, id);
}

userver::formats::json::ValueBuilder FillProductException(
    const std::string& product_id, const std::string& code) {
  userver::formats::json::ValueBuilder builder;
  builder["problem"] = code;
  builder["item_id"] = product_id;
  return builder;
}

std::string FillAllProductsException(std::vector<std::string> product_ids,
                                     const std::string& code) {
  userver::formats::json::ValueBuilder builder{
      userver::formats::common::Type::kArray};
  for (const auto& product_id : product_ids) {
    builder.PushBack(FillProductException(product_id, code));
  }
  return userver::formats::json::ToString(builder.ExtractValue());
};

class Check final : public userver::server::handlers::HttpHandlerBase {
 public:
  static constexpr std::string_view kName = "handler-check";

  Check(const userver::components::ComponentConfig& config,
        const userver::components::ComponentContext& component_context)
      : HttpHandlerBase(config, component_context),
        pg_cluster_(
            component_context
                .FindComponent<userver::components::Postgres>("postgres-db-1")
                .GetCluster()) {}

  /// Форматирует ответ
  std::string MakeResponse(std::vector<std::string> product_ids,
                           const std::string& user_id) const {
    std::unique_ptr<models::User> user;
    try {
      user = models::CreateUser(std::stoi(user_id), pg_cluster_);
    } catch (const models::NoUserException& e) {
      // Если пользователь не найден - заполяем все продукты с ошибкой из
      // исключения NoUserException
      return FillAllProductsException(product_ids, e.what());
    }

    std::vector<std::unique_ptr<models::Product>> products;
    products.reserve(product_ids.size());
    userver::formats::json::ValueBuilder builder{
        userver::formats::common::Type::kArray};

    // Достаем продукты из базы и конвертируем их в объекты
    for (const auto& product_id : product_ids) {
      auto [product_type, product_id_int] = parceProductId(product_id);
      try {
        auto product =
            models::CreateProduct(product_id_int, product_type, pg_cluster_);
        products.emplace_back(std::move(product));
      } catch (const models::CustomException& e) {
        // Если есть какие-то проблемы с созданием продукты - добавляем его в
        // ответ
        builder.PushBack(FillProductException(product_id, e.what()));
      }
    }

    // добавляем невалидные продукты в ответ.
    for (const auto& product : products) {
      try {
        product->IsValid(user);
      } catch (const models::CustomException& e) {
        builder.PushBack(FillProductException(product->GetFullId(), e.what()));
      }
    }

    return userver::formats::json::ToString(builder.ExtractValue());
  };

  /// Точка входа при обработке get запроса.
  std::string HandleRequestThrow(
      const userver::server::http::HttpRequest& request,
      userver::server::request::RequestContext&) const override {
    const auto& user_id = request.GetArg("user_id");
    const auto& product_ids = request.GetArgVector("item_id");
    try {
      return MakeResponse(product_ids, user_id);
    } catch (const std::exception& e) {
      LOG_ERROR() << e.what();

      // В любой непонятной ситуации заполняем все продукты как WRONG_DATA
      return FillAllProductsException(product_ids, "WRONG_DATA");
    }
  }

  userver::storages::postgres::ClusterPtr pg_cluster_;
};

}  // namespace

void AppendCheck(userver::components::ComponentList& component_list) {
  component_list.Append<Check>();
  component_list.Append<userver::components::Postgres>("postgres-db-1");
  component_list.Append<userver::clients::dns::Component>();
}

}  // namespace code_architecture
