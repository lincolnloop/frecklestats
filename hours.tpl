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

<script src="http://code.jquery.com/jquery-2.0.3.min.js"></script>
<script src="http://code.highcharts.com/highcharts.js"></script>
<div id="container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
<script>
$(function () {
        $('#container').highcharts({
            chart: {
                type: 'area'
            },
            xAxis: {
                tickmarkPlacement: 'on',
                title: {
                    enabled: false
                }
            },
            yAxis: {
                title: {
                    text: 'Billions'
                },
                labels: {
                    formatter: function() {
                        return this.value / 1000;
                    }
                }
            },
            tooltip: {
                shared: true,
                valueSuffix: ' millions'
            },
            plotOptions: {
                area: {
                    stacking: 'normal',
                    lineColor: '#666666',
                    lineWidth: 1,
                    marker: {
                        lineWidth: 1,
                        lineColor: '#666666'
                    }
                }
            },
            series: [
            {% for k, v in hours_project.iteritems() %}
            {
                name: '{{ k }}',
                data: {{ v }}
            },
            {% endfor %}]
        });
    });


</script>



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