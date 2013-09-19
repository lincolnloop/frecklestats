<!DOCTYPE html>
<html>
<head>
    <meta charset=utf-8 />
    <title>Hours</title>
    <style type="text/css">
    pre{ margin: 0;}
    </style>
</head>
<body>


<div style="font-size: 30px; padding: 40px;">
	You worked <strong>{{ summary.hours_done }}</strong> hours this week. There are
	<strong>{{ summary.hours_todo }}</strong> hours to do. That is {{ summary.hours_per_day_todo }} hours
	per day for the next {{ summary.days_left }} days.
</div>

<hr/>

{{ summary }}

<ul>
{% for id, name in projects.iteritems() %}
    <li>{{ name }}</li>
{% endfor %}
</ul>

<hr/>

<ul>
{% for h in hours %}
    <li><pre>{{ h.datetime }}: {{ h.minutes }}	({{ h.project }})</pre></li>
{% endfor %}
</ul>

<hr/>

</body>
</html>