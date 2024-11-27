#include "auth.hpp"

namespace bookmarker {

std::optional<TSession> GetSessionInfo(
    userver::storages::postgres::ClusterPtr pg_cluster,
    const userver::server::http::HttpRequest& request
) {
    if (!request.HasHeader(USER_TICKET_HEADER_NAME)) {
        return std::nullopt;
    }

    auto id = request.GetHeader(USER_TICKET_HEADER_NAME);
    auto result = pg_cluster->Execute(
        userver::storages::postgres::ClusterHostType::kMaster,
        "SELECT * FROM bookmarker.auth_sessions "
        "WHERE id = $1 ",
        id
    );

    if (result.IsEmpty()) {
        return std::nullopt;
    }

    return result.AsSingleRow<TSession>(userver::storages::postgres::kRowTag);
}

}  // namespace bookmarker