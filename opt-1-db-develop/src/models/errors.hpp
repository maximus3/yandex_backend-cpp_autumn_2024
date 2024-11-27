#include <exception>
#include <string>

namespace code_architecture::models {

class CustomException : public std::exception {
 public:
  CustomException(const std::string& code) : code_(code) {}

  virtual const char* what() const noexcept override { return code_.c_str(); }

 private:
  std::string code_;
};

class WrongDataException : public CustomException {
 public:
  WrongDataException() : CustomException("WRONG_DATA") {}
};

class ItemNotFoundException : public CustomException {
 public:
  ItemNotFoundException() : CustomException("ITEM_NOT_FOUND") {}
};

class NoUserException : public CustomException {
 public:
  NoUserException() : CustomException("NO_USER") {}
};

class NoReceiptException : public CustomException {
 public:
  NoReceiptException() : CustomException("NO_RECEIPT") {}
};

class ItemIsSpecialException : public CustomException {
 public:
  ItemIsSpecialException() : CustomException("ITEM_IS_SPECIAL") {}
};

class ItemSpecialWrongSpecificException : public CustomException {
 public:
  ItemSpecialWrongSpecificException()
      : CustomException("ITEM_SPECIAL_WRONG_SPECIFIC") {}
};

}  // namespace code_architecture::models