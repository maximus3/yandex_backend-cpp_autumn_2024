#include "hello.hpp"

#include <userver/utest/utest.hpp>

UTEST(SayHelloTo, Basic) {
  // Проверяем, что функция SayHelloTo делает то, что было задумано
  EXPECT_EQ(service_hello::SayHelloTo("Developer"), "Hello, Developer!\n");
}
