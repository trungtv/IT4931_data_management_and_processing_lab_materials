{% macro vwap(price_column, quantity_column) %}
sum({{ price_column }} * {{ quantity_column }}) / sum({{ quantity_column }})
{% endmacro %}
