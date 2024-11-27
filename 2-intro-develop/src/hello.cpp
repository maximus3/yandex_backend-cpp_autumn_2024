#include "hello.hpp"

#include <fmt/format.h>

#include <userver/server/handlers/http_handler_base.hpp>

namespace service_hello {

namespace {

class Hello final : public userver::server::handlers::HttpHandlerBase {
public:
  static constexpr std::string_view kName = "handler-v1-hello";

  using HttpHandlerBase::HttpHandlerBase;

  std::string HandleRequestThrow(
      const userver::server::http::HttpRequest &request,
      userver::server::request::RequestContext &) const override {
    // Берём тело из запроса
    auto request_body =
        userver::formats::json::FromString(request.RequestBody());

    // Читаем name из тела запроса
    // name будет иметь тип std::optional<std::string>
    auto name = request_body["name"].As<std::optional<std::string>>();

    // Проверяем, передали ли нам name
    if (!name.has_value()) {
      // Если нет - возвращаем ошибку 400
      auto& response = request.GetHttpResponse();
      response.SetStatus(userver::server::http::HttpStatus::kBadRequest);
      return {};
    }
    
    // Если передали - возвращаем текст
    return service_hello::SayHelloTo(name.value());
  }
};

} // namespace

std::string SayHelloTo(std::string_view name) {
  // Здесь намеренно заложена ошибка, её надо исправить, чтобы сдать задание
  return fmt::format("Hi, {}!\n", name);
}

void AppendHello(userver::components::ComponentList &component_list) {
  component_list.Append<Hello>();
}

} // namespace service_hello
