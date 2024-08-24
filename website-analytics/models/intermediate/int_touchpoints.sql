select distinct sessions.visitor_id,
       -- first
       FIRST_VALUE(sessions.source_medium) OVER (PARTITION BY sessions.visitor_id ORDER BY sessions.timestamp) AS first_source_medium,
       FIRST_VALUE(sessions.utm_campaign) OVER (PARTITION BY sessions.visitor_id ORDER BY sessions.timestamp) AS first_utm_campaign,
       FIRST_VALUE(events.event_url) OVER (PARTITION BY sessions.visitor_id ORDER BY sessions.timestamp) AS first_event_url,
       -- last
       LAST_VALUE(sessions.source_medium) OVER (PARTITION BY sessions.visitor_id ORDER BY sessions.timestamp desc) AS last_source_medium,
       LAST_VALUE(sessions.utm_campaign) OVER (PARTITION BY sessions.visitor_id ORDER BY sessions.timestamp desc) AS last_utm_campaign,
       LAST_VALUE(events.event_url) OVER (PARTITION BY sessions.visitor_id ORDER BY events.timestamp desc) AS last_event_url
from {{ref('int_sessions')}} as sessions
left join {{ref('int_events')}} as events
    on sessions.session_id = events.session_id