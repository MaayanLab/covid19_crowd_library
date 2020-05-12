total = d => d.reduce((total, arg) => total + arg.count, 0);
cumulative_sum = d => d.map((e, i) => ({date: e.date, count: total(d.slice(0, i + 1))}))
spark = (data, wrapper, label) => {
    const x = d3.scaleLinear()
    const y = d3.scaleLinear()
    const style = ({
        line: {
            stroke: "#444",
            strokeWidth: 0.7
        },
        circle: {
            fill: "#f00",
            stroke: "none"
        },
        label: {
            font: ".5em sans-serif"
        },
        margin: {
            left: 5,
            right: 55,
            top: 5,
            bottom: 5
        },
        dim: {
            width: 100,
            height: 30
        }
    })
    const dateParse = d3.timeParse('%Y-%m-%d')
    const xScale = x
        .range([style.margin.left, style.dim.width - style.margin.right])
        .domain(d3.extent(data, d => dateParse(d.date)));

    const yScale = y
        .range([style.dim.height - style.margin.bottom, style.margin.top])
        .domain(d3.extent(data, d => d.count));

    const last = {
        x: xScale(dateParse(data[data.length - 1].date)),
        y: yScale(data[data.length - 1].count)
    };

    const svg = d3.select(wrapper)
        .attr("width", style.dim.width)
        .attr("height", style.dim.height)
        .attr("viewBox", [0, 0, style.dim.width, style.dim.height]);

    const g = svg
        .append("g");

    const line = d3
        .line()
        .curve(d3.curveMonotoneX)
        .x(d => xScale(dateParse(d.date)))
        .y(d => yScale(d.count));

    const path = g
        .append("path")
        .datum(data)
        .attr("d", line)
        .style("fill", "none")
        .style("stroke", style.line.stroke)
        .style("stroke-width", style.line.strokeWidth);

    const current = g
        .append("g")
        .attr("transform", `translate(${last.x},${last.y})`);

    const curr_circle = current
        .append("circle")
        .attr("r", 1.5)
        .style("fill", style.circle.fill)
        .style("stroke", style.circle.stroke);

    console.log(data[data.length-1])

    if (label === 'today') {
        let today = new Date()
        today.setTime(today.getTime() + today.getTimezoneOffset()*60*1000)
        let today_intl = Intl.DateTimeFormat('en-US').format(today)
        let last_day = new Date(data[data.length - 1].date)
        last_day.setTime(last_day.getTime() + last_day.getTimezoneOffset()*60*1000)
        let last_day_intl = Intl.DateTimeFormat('en-US').format(last_day)
        if (today_intl !== last_day_intl){
            label = `at ${last_day}`;
            style.label.font = ".45em sans-serif"
        }
    }

    const curr_label_n = current
        .append("text")
        .attr("text-anchor", "right")
        .attr("dy", ".35em")
        .attr("pointer-events", "none")
        .attr("x", 5)
        .style("fill", style.circle.fill)
        .style("font", style.label.font)
        .text(`${data[data.length - 1].count} ${label}`);

    return svg.node();
}