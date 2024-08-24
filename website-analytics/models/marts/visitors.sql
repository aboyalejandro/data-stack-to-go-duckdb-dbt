select distinct sessions.visitor_id,
       sessions.country,
       -- first
       touchpoints.first_source_medium,
       touchpoints.first_utm_campaign,
       touchpoints.first_event_url,
       -- last
       touchpoints.last_source_medium,
       touchpoints.last_utm_campaign,
       touchpoints.last_event_url,
       -- arrays
       array_agg(sessions.source_medium order by sessions.timestamp) as all_source_mediums,
       array_agg(sessions.utm_campaign order by sessions.timestamp) as all_campaigns,
       array_agg(events.event_url order by events.timestamp) as all_event_urls,
       -- metrics
       count (distinct sessions.session_id) as total_sessions,
       sum(sessions.session_total_page_views) as session_total_page_views,
       sum(sessions.session_total_events) as session_total_events,
       sessions.visitor_days_since_last_session,
       sessions.visitor_days_since_first_session,
       current_timestamp as date_transformed
from {{ref('int_sessions')}} as sessions
left join {{ref('int_events')}} as events
    on sessions.session_id = events.session_id
left join {{ref('int_touchpoints')}} as touchpoints
    on sessions.visitor_id = touchpoints.visitor_id
group by all