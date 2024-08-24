select {{dbt_utils.generate_surrogate_key(['sessions.visitor_id',
                                           'sessions.session_id',
                                           'events.event_id',
                                           'events.timestamp'])}} as s_id,
       sessions.visitor_id,
       sessions.session_id,
       sessions.visitor_session_number,
       case when sessions.visitor_session_number = 1 then true else false end as is_first_session,
       events.event_id,
       events.page_view_index,
       events.timestamp,
       events.event_url,
       sessions.is_returning,
       sessions.country,
       sessions.source_medium,
       sessions.utm_campaign,
       sessions.session_total_page_views,
       sessions.session_total_events,
       current_timestamp as date_transformed
from {{ref('int_sessions')}} as sessions
left join {{ref('int_events')}} as events
on sessions.session_id = events.session_id