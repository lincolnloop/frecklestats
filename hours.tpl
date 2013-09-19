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

    <h1>
        Hours
    </h1>

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

You worked <strong>12 hours</strong> this week. <strong>18 more hours</strong> to do
in the next <strong>3 days</strong> (<strong>6 hours per day</strong>).

</body>
</html>