function range(n) {
    return Array.apply(null, {length: n}).map(Number.call, Number);
}

function drawChart(xdata, ydata, xlabel, ylabel, id_parent, w, h, color) {

    // Default parameters
    id_parent = typeof id_parent !== 'undefined' ? id_parent : 'body';
    w = typeof w !== 'undefined' ? w : 300;
    h = typeof h !== 'undefined' ? h : 200;
    xlabel = typeof xlabel !== 'undefined' ? xlabel : 'x';
    ylabel = typeof ylabel !== 'undefined' ? ylabel : 'y';
    color = typeof color !== 'undefined' ? color : '#c00';

    // Scaling the axis
    var max = d3.max(ydata);
    var x  = d3.scale.linear().domain([0, xdata.length - 1]).range([0, w]);
    var y  = d3.scale.linear().domain([0, max]).range([h, 0]);
    var yticks = 7;
    var xticks = 7;

    // Creating the SVG
    var vis = d3.select(id_parent)
    .append('div')
    .attr('class', 'chart')
    .append('svg:svg')
    .attr('width', w)
    .attr('height', h);

    // Drawing the path
    vis.selectAll('path.line')
    .data([ydata])
    .enter().append("svg:path")
    .attr("d", d3.svg.line().x(function (d, i) { return x(i); }).y(function (d) { return y(d); }));

    // The domains
    vis.append("svg:text")
    .text(ylabel)
    .attr('dy', -10)
    .attr('dx', -0)
    // .attr('transform', "rotate(270)")
    .attr("class", "domain");

    vis.append("svg:text")
    .text(xlabel)
    .attr('dy', h + 40)
    .attr('dx', w / 2)
    .attr('text-anchor', 'middle')
    .attr("class", "domain");

    // The ticks
    ticks = vis.selectAll('.tick')
    .data(y.ticks(yticks))
    .enter().append('svg:g')
    .attr('transform', function (d) {  return "translate(0, " + y(d) + ")"; })
    .attr('class', 'tick');

    ticks2 = vis.selectAll('.tick2')
    .data(x.ticks(xticks))
    .enter().append('svg:g')
    .attr('transform', function (d, i) {  return "translate(" + x(d) + ", 0)"; })
    .attr('class', 'tick2');

    ticks.append('svg:line')
    .attr('y1', 0)
    .attr('y2', 0)
    .attr('x1', 0)
    .attr('x2', w);

    ticks2.append('svg:line')
    .attr('y1', 0)
    .attr('y2', h)
    .attr('x1', 0)
    .attr('x2', 0);

    ticks.append('svg:text')
    .text(function (d) { return d; })
    .attr('text-anchor', 'end')
    .attr('dy', 2)
    .attr('dx', -4);

    ticks2.append('svg:text')
    .data(x.ticks(xticks))
    .text(function (d) { return d; })
    .attr('text-anchor', 'end')
    .attr('dy', h + 20)
    .attr('dx', 4);

    vis.selectAll('.point')
    .data(ydata)
    .enter().append("svg:circle")
    // .attr("class", function (d, i) { if (d == max) { return 'point max'; } else { return 'point'; }})
    .attr("class", "point")
    .attr("cx", function (d, i) { return x(i); })
    .attr("cy", function (d) { return y(d); })
    // .attr("r", function (d, i) { if (d == max) { return 10; } else { return 6; }});
    .attr("r", 4);
}


function drawScatterChart(xdata, ydata, xlabel, ylabel, id_parent, w, h) {

    // Default parameters
    id_parent = typeof id_parent !== 'undefined' ? id_parent : 'body';
    w = typeof w !== 'undefined' ? w : 1000;
    h = typeof h !== 'undefined' ? h : 500;
    xlabel = typeof xlabel !== 'undefined' ? xlabel : 'x';
    ylabel = typeof ylabel !== 'undefined' ? ylabel : 'y';

    var xmax = d3.max(xdata);
    var xmin = Math.min(0, d3.min(xdata));
    var ymax = d3.max(ydata);
    var ymin = Math.min(0, d3.min(ydata));


    var x = d3.scale.linear().domain([xmin, xmax]).range([0, w]);
    var y = d3.scale.linear().domain([ymin, ymax]).range([h, 0]);

    var xticks = 7;
    var yticks = 7;

    var vis = d3.select("#objective-function")
    .append('div')
    .attr('class', 'chart')
    .append('svg:svg')
    .attr('width', w)
    .attr('height', h);

    // The domains
    vis.append("svg:text")
    .text(ylabel)
    .attr('dy', -10)
    .attr('dx', -0)
    // .attr('transform', "rotate(270)")
    .attr("class", "domain");

    vis.append("svg:text")
    .text(xlabel)
    .attr('dy', h + 40)
    .attr('dx', w / 2)
    .attr('text-anchor', 'middle')
    .attr("class", "domain");

    ticks = vis.selectAll('.tick')
    .data(y.ticks(yticks))
    .enter().append('svg:g')
    .attr('transform', function (d) {  return "translate(0, " + y(d) + ")"; })
    .attr('class', 'tick');

    ticks2 = vis.selectAll('.tick2')
    .data(x.ticks(xticks))
    .enter().append('svg:g')
    .attr('transform', function (d, i) {  return "translate(" + x(d) + ", 0)"; })
    .attr('class', 'tick2');

    ticks.append('svg:line')
    .attr('y1', 0)
    .attr('y2', 0)
    .attr('x1', 0)
    .attr('x2', w);

    ticks2.append('svg:line')
    .attr('y1', 0)
    .attr('y2', h)
    .attr('x1', 0)
    .attr('x2', 0);

    ticks.append('svg:text')
    .text(function (d) { return d; })
    .attr('text-anchor', 'end')
    .attr('dy', 2)
    .attr('dx', -4);

    ticks2.append('svg:text')
    .data(x.ticks(xticks))
    .text(function (d) { return d; })
    .attr('text-anchor', 'end')
    .attr('dy', h + 20)
    .attr('dx', 4);


    vis.selectAll('.point2')
    .data(ydata)
    .enter().append("svg:circle")
    .attr("class", "point2")
    .data(xdata)
    .attr("cx", function (d) { return x(d); })
    .data(ydata)
    .attr("cy", function (d) { return y(d); })
    .attr("r", 4);

}
