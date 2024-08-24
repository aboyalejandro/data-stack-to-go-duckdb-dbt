{% macro country_group(country) %}
    case 
        when {{country}} = 'United Stated' then {{country}}
        when {{country}} = 'Netherlands' then {{country}}
        when {{country}} = 'Ireland' then {{country}}
        when {{country}} = 'Canada' then {{country}}
        when {{country}} = 'Belgium' then {{country}}
        when {{country}} = 'China' then {{country}}
        else 'Other'
    end
{% endmacro %}