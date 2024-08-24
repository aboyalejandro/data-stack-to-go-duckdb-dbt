select session_id,
       visitor_id,
       timestamp::timestamp as timestamp,
       visitor_session_number::int as visitor_session_number,
       {{is_returning('visitor_returning')}} as is_returning,
       {{country_group('location_country_name')}} as country,
       source_medium,
       campaign_name as utm_campaign,
       session_total_page_views::int as session_total_page_views,
       session_total_events::int as session_total_events,
       visitor_days_since_last_session::int as visitor_days_since_last_session,
       visitor_days_since_first_session::int as visitor_days_since_first_session,
       current_timestamp as date_transformed
from {{ref('stg_sessions')}}