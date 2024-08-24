{% snapshot visitors_snapshot %}

{{
    config(
      target_schema='main',
      unique_key='visitor_id',
      strategy='check',
      check_cols = ['country','last_source_medium','last_utm_campaign','last_event_url']
    )
}}

select * from {{ref('visitors')}} 

{% endsnapshot %}