function range(n) {
    return Array.apply(null, {length: n}).map(Number.call, Number);
}

function drawChart(xdata, ydata, xlabel, ylabel, id_parent, w, h, color) {

    // Default parameters
    id_parent = typeof id_parent !== 'undefined' ? id_parent : 'body';
    w = typeof w !== 'undefined' ? w : 400;
    h = typeof h !== 'undefined' ? h : 200;
    xlabel = typeof xlabel !== 'undefined' ? xlabel : 'x';
    ylabel = typeof ylabel !== 'undefined' ? ylabel : 'y';
    color = typeof color !== 'undefined' ? color : '#c00';

    // Scaling the axis
    var max = d3.max(ydata);
    var x  = d3.scale.linear().domain([0, xdata.length - 1]).range([0, w]);
    var y  = d3.scale.linear().domain([0, max]).range([h, 0]);

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
    .style("stroke", color)
    .attr("d", d3.svg.line().x(function (d, i) { return x(i); }).y(function (d) { return y(d); }));

    // The domains
    vis.append("svg:text")
    .text(ylabel)
    .attr('dy', 18)
    .attr('dx', -4)
    .attr('text-anchor', 'end')
    .attr('transform', "rotate(270)")
    .attr("class", "domain");

    vis.append("svg:text")
    .text(xlabel)
    .attr('dy', h - 5)
    .attr('dx', w - 5)
    .attr('text-anchor', 'end')
    .attr("class", "domain");

    // The ticks
    ticks = vis.selectAll('.tick')
    .data(y.ticks(7))
    .enter().append('svg:g')
    .attr('transform', function (d) {  return "translate(0, " + y(d) + ")"; })
    .attr('class', 'tick');

    ticks2 = vis.selectAll('.tick2')
    .data(x.ticks(xdata.length - 2))
    .enter().append('svg:g')
    .attr('transform', function (d, i) {  return "translate(" + x(i) + ", 0)"; })
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
    .data(xdata)
    .text(function (d) { return d; })
    .attr('text-anchor', 'end')
    .attr('dy', h + 20)
    .attr('dx', 4);

    vis.selectAll('.point')
    .data(ydata)
    .enter().append("svg:circle")
    .attr("class", function (d, i) { if (d == max) { return 'point max'; } else { return 'point'; }})
    .attr("cx", function (d, i) { return x(i); })
    .attr("cy", function (d) { return y(d); })
    .attr("r", function (d, i) { if (d == max) { return 10; } else { return 6; }});
}

