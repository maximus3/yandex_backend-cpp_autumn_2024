#pragma once

#include <memory>
#include <string>

#include <userver/storages/postgres/cluster.hpp>

#include <userver/components/component_list.hpp>

#include "common_user.hpp"

namespace code_architecture::models {

/// Обычный товар
/// Доступен всем
class Product {
 public:
  Product(int id);

  /// Проверяет, доступен ли обычный товар пользователю
  virtual bool IsValid(const std::unique_ptr<User>& user) const;

  virtual std::string GetFullId() const;

  /// Возвращает указатель на продукт, если в базе есть обычный продукт с
  /// нужным id. Иначе Кидает исключение.
  static std::unique_ptr<Product> GetIfExists(
      int id, const userver::storages::postgres::ClusterPtr& pg_cluster);

  virtual ~Product() = default;

 protected:
  int id_;

 private:
  static const std::string type_;
};

/// Товар по рецепту
/// Доступен только пользователям с рецептом и всем врачам
class ReceiptProduct : public Product {
 public:
  ReceiptProduct(int id);

  /// Проверяет, доступен ли товар по рецепту пользователю
  bool IsValid(const std::unique_ptr<User>& user) const override;

  /// Проверяет, если ли среди переданных рецептов рецепт для данного товара.
  bool HasPermitionToBuy(const std::unordered_set<int>& user_receipts) const;

  std::string GetFullId() const override final;

  /// Возвращает указатель на продукт, если в базе есть продукт по рецепту с
  /// нужным id. Иначе Кидает исключение.
  static std::unique_ptr<Product> GetIfExists(
      int id, const userver::storages::postgres::ClusterPtr& pg_cluster);

  virtual ~ReceiptProduct() = default;

 private:
  static const std::string type_;
};

/// Специальный товар
/// Доступен только врачам с определенной специальностью
class SpecialProduct : public Product {
 public:
  SpecialProduct(int id, int speciality_id);

  /// Проверяет, доступен ли специальный товар пользователю
  bool IsValid(const std::unique_ptr<User>& user) const override;

  /// Проверяет, соответствует ли переданная специальность специальности для
  /// данного товара.
  bool HasPermitionToBuy(int speciality_id) const;

  std::string GetFullId() const override final;

  /// Возвращает указатель на продукт, если в базе есть специальный продукт с
  /// нужным id. Иначе Кидает исключение.
  static std::unique_ptr<Product> GetIfExists(
      int id, const userver::storages::postgres::ClusterPtr& pg_cluster);

  virtual ~SpecialProduct() = default;

 private:
  int speciality_id_;
  static const std::string type_;
};

/// Возвращает указатель на продукт, если в базе есть продукт с нужным id и
/// type. Иначе Кидает исключение.
std::unique_ptr<Product> CreateProduct(
    int id, const std::string& type,
    const userver::storages::postgres::ClusterPtr& pg_cluster);

}  // namespace code_architecture::models
