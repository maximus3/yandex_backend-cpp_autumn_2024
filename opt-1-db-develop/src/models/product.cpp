#include "product.hpp"

#include <memory>
#include <string>

#include <fmt/compile.h>
#include <fmt/format.h>

#include <userver/clients/dns/component.hpp>
#include <userver/components/component.hpp>
#include <userver/decimal64/decimal64.hpp>
#include <userver/logging/log.hpp>
#include <userver/server/handlers/http_handler_base.hpp>
#include <userver/storages/postgres/cluster.hpp>
#include <userver/storages/postgres/component.hpp>
#include <userver/storages/postgres/result_set.hpp>
#include <userver/utils/assert.hpp>

#include "errors.hpp"

namespace code_architecture::models {

namespace {

struct SpecialItemRow {
  int id;
  std::optional<std::string> name;
  std::optional<int> amount;
  std::optional<userver::decimal64::Decimal<8>> price;
  std::optional<std::string> dosage_form;
  std::optional<std::string> manufacturer;
  std::optional<std::string> barcode;
  std::optional<int> speciality_id;
};

userver::storages::postgres::ResultSet GetResultSet(
    int id, const std::string& type,
    const userver::storages::postgres::ClusterPtr& pg_cluster) {
  return pg_cluster->Execute(
      userver::storages::postgres::ClusterHostType::kSlaveOrMaster,
      fmt::format("SELECT * FROM code_architecture.{}_item"
                  " WHERE id = $1",
                  type),
      id);
}

}  // namespace

const std::string Product::type_ = "common";
const std::string ReceiptProduct::type_ = "receipt";
const std::string SpecialProduct::type_ = "special";

Product::Product(int id) : id_{id} {};
ReceiptProduct::ReceiptProduct(int id) : Product{id} {};
SpecialProduct::SpecialProduct(int id, int speciality_id)
    : Product{id}, speciality_id_{speciality_id} {};

std::unique_ptr<Product> Product::GetIfExists(
    int id, const userver::storages::postgres::ClusterPtr& pg_cluster) {
  auto result = GetResultSet(id, type_, pg_cluster);
  if (result.IsEmpty()) {
    throw ItemNotFoundException();
  }
  return std::make_unique<Product>(id);
}

std::unique_ptr<Product> ReceiptProduct::GetIfExists(
    int id, const userver::storages::postgres::ClusterPtr& pg_cluster) {
  auto result = GetResultSet(id, type_, pg_cluster);
  if (result.IsEmpty()) {
    throw ItemNotFoundException();
  }
  return std::make_unique<ReceiptProduct>(id);
}

std::unique_ptr<Product> SpecialProduct::GetIfExists(
    int id, const userver::storages::postgres::ClusterPtr& pg_cluster) {
  auto result = GetResultSet(id, type_, pg_cluster);
  if (result.IsEmpty()) {
    throw ItemNotFoundException();
  }
  auto specialty_id =
      result.AsSingleRow<SpecialItemRow>(userver::storages::postgres::kRowTag)
          .speciality_id;
  if (!specialty_id.has_value()) {
    throw WrongDataException();
  }
  return std::make_unique<SpecialProduct>(id, specialty_id.value());
}

std::unique_ptr<Product> CreateProduct(
    int id, const std::string& type,
    const userver::storages::postgres::ClusterPtr& pg_cluster) {
  if (type == "common") {
    return Product::GetIfExists(id, pg_cluster);
  } else if (type == "receipt") {
    return ReceiptProduct::GetIfExists(id, pg_cluster);
  } else if (type == "special") {
    return SpecialProduct::GetIfExists(id, pg_cluster);
  } else {
    throw WrongDataException();
  }
}

bool SpecialProduct::HasPermitionToBuy(int speciality_id) const {
  return this->speciality_id_ == speciality_id;
}

bool Product::IsValid(const std::unique_ptr<User>& user) const {
  return user->IsProductValid(*this);
}

bool SpecialProduct::IsValid(const std::unique_ptr<User>& user) const {
  return user->IsProductValid(*this);
}

bool ReceiptProduct::IsValid(const std::unique_ptr<User>& user) const {
  return user->IsProductValid(*this);
}

bool ReceiptProduct::HasPermitionToBuy(
    const std::unordered_set<int>& user_receipts) const {
  return user_receipts.find(id_) != user_receipts.end();
}

std::string Product::GetFullId() const {
  return fmt::format("{}_{}", type_, id_);
}
std::string ReceiptProduct::GetFullId() const {
  return fmt::format("{}_{}", type_, id_);
}
std::string SpecialProduct::GetFullId() const {
  return fmt::format("{}_{}", type_, id_);
}

}  // namespace code_architecture::models
