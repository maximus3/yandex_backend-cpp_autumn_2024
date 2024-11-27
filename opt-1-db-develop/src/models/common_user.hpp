#pragma once

#include <memory>
#include <optional>

#include <userver/storages/postgres/cluster.hpp>

#include <userver/components/component_list.hpp>

namespace code_architecture::models {
class Product;
class SpecialProduct;
class ReceiptProduct;

/// Обычный пользователь
/// Может иметь рецепты
class User {
 public:
  User(int id, std::unordered_set<int>&& reciped_products = {});

  virtual ~User() = default;

  /// Возвращает объект Пользователя, если в базе есть пользователь с нужным id.
  /// Иначе nullopt.
  static std::optional<User> GetIfExists(
      int id, const userver::storages::postgres::ClusterPtr& pg_cluster);

  /// Проверяем, может ли пользователь купить обычный продукт
  /// Иначе кидаем исключение.
  virtual bool IsProductValid(const Product& product) const;

  /// Проверяем, может ли пользователь купить продукт по рецепту
  /// Иначе кидаем исключение.
  virtual bool IsProductValid(const ReceiptProduct& product) const;

  /// Проверяем, может ли пользователь купить специальный продукт.
  /// Иначе кидаем исключение.
  virtual bool IsProductValid(const SpecialProduct& product) const;

 private:
  int id_;
  std::unordered_set<int> receipted_products_;
};

/// Врач
/// Имеет специальность
class Doctor : public User {
 public:
  Doctor(int id, int speciality_id);

  /// Возвращает объект Доктора, если в базе есть доктор с нужным id.
  /// Иначе nullopt.
  static std::optional<Doctor> GetIfExists(
      int id, const userver::storages::postgres::ClusterPtr& pg_cluster);

  /// Проверяем, может ли врач купить обычный продукт
  /// Иначе кидаем исключение.
  bool IsProductValid(const Product& product) const final override;

  /// Проверяем, может ли врач купить продукт по рецепту
  /// Иначе кидаем исключение.
  bool IsProductValid(const ReceiptProduct& product) const final override;

  /// Проверяем, может ли врач купить специальный продукт.
  /// Иначе кидаем исключение.
  bool IsProductValid(const SpecialProduct& product) const final override;

  virtual ~Doctor() = default;

 private:
  int speciality_id;
};

/// Возвращает указатель на Пользователя, если в базе есть пользователь с нужным
/// id. Иначе Кидает исключение.
std::unique_ptr<User> CreateUser(
    int user_id, const userver::storages::postgres::ClusterPtr& pg_cluster);

}  // namespace code_architecture::models
