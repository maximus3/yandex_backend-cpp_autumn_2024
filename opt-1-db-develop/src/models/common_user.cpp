#include "common_user.hpp"

#include <fmt/format.h>

#include <memory>
#include <optional>
#include <stdexcept>
#include <unordered_set>
#include <userver/clients/dns/component.hpp>
#include <userver/components/component.hpp>
#include <userver/logging/log.hpp>
#include <userver/server/handlers/http_handler_base.hpp>
#include <userver/storages/postgres/cluster.hpp>
#include <userver/storages/postgres/component.hpp>
#include <userver/utils/assert.hpp>
#include "errors.hpp"
#include "product.hpp"

namespace code_architecture::models {

User::User(int id, std::unordered_set<int>&& reciped_products)
    : id_{id}, receipted_products_{std::move(reciped_products)} {};

std::optional<User> User::GetIfExists(
    int id, const userver::storages::postgres::ClusterPtr& pg_cluster) {
  auto result = pg_cluster->Execute(
      userver::storages::postgres::ClusterHostType::kSlaveOrMaster,
      "SELECT * FROM code_architecture.user_account"
      " WHERE id = $1",
      id);
  if (result.IsEmpty()) {
    return std::nullopt;
  }
  std::unordered_set<int> reciped_products;
  auto receipts_result = pg_cluster->Execute(
      userver::storages::postgres::ClusterHostType::kSlaveOrMaster,
      "SELECT * FROM code_architecture.receipt"
      " WHERE user_id = $1",
      id);
  for (const auto& row : receipts_result) {
    auto receipted_item = row["item_id"].As<int>();
    reciped_products.insert(receipted_item);
  }
  return User{id, std::move(reciped_products)};
}

Doctor::Doctor(int id, int speciality_id)
    : User{id}, speciality_id{speciality_id} {};

std::optional<Doctor> Doctor::GetIfExists(
    int id, const userver::storages::postgres::ClusterPtr& pg_cluster) {
  auto result = pg_cluster->Execute(
      userver::storages::postgres::ClusterHostType::kSlaveOrMaster,
      "SELECT * FROM code_architecture.doctor_account"
      " WHERE id = $1",
      id);
  if (!result.IsEmpty()) {
    auto specialty_id = result.Front()["specialty_id"].As<int>();
    return Doctor{id, specialty_id};
  }

  return std::nullopt;
}

std::unique_ptr<User> CreateUser(
    int user_id, const userver::storages::postgres::ClusterPtr& pg_cluster) {
  auto simple_user = User::GetIfExists(user_id, pg_cluster);
  auto doctor_user = Doctor::GetIfExists(user_id, pg_cluster);

  if (simple_user.has_value() && doctor_user.has_value()) {
    throw std::runtime_error(
        "User cannot be in simple users and doctors tables at the same time");
  } else if (simple_user.has_value()) {
    return std::make_unique<User>(simple_user.value());
  } else if (doctor_user.has_value()) {
    return std::make_unique<Doctor>(doctor_user.value());
  }
  throw NoUserException();
}

bool User::IsProductValid(const Product& product) const {
  // Опишите здесь стратегию валидации
  return false;
}

  bool User::IsProductValid(const ReceiptProduct& product) const {
    // Опишите здесь стратегию валидации
    return false;
  }

  bool User::IsProductValid(const SpecialProduct& product) const {
    // Опишите здесь стратегию валидации
    return false;
  }

  bool Doctor::IsProductValid(const Product& product) const {
    // Опишите здесь стратегию валидации
    return false;
  }

  bool Doctor::IsProductValid(const ReceiptProduct& product) const {
    // Опишите здесь стратегию валидации
    return false;
  }

  bool Doctor::IsProductValid(const SpecialProduct& product) const {
    // Опишите здесь стратегию валидации
    return false;
  }

}  // namespace code_architecture::models
