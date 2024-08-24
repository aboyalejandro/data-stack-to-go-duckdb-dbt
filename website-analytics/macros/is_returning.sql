{% macro is_returning(column) %}
    case when {{column}} = 'Returning' then true else false end
{% endmacro %}

