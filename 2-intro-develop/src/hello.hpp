#pragma once

#include <string>
#include <string_view>

#include <userver/components/component_list.hpp>

namespace service_hello {

std::string SayHelloTo(std::string_view name);

void AppendHello(userver::components::ComponentList &component_list);

} // namespace service_hello
