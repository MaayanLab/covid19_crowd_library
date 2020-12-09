function chart(data, type, numBar, fill, width = 600) {
    const svg_wrapper = `#${type}_bargraph`
    data = data.sort((a, b) => d3.descending(a.count, b.count)).slice(0, numBar);
    data.format = "d"
    const margin = ({top: 20, right: 30, bottom: 20, left: 100})
    const barHeight = 16
    height = Math.ceil((data.length + 0.1) * barHeight) + margin.top + margin.bottom

    const x = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.count)])
        .range([margin.left, width - margin.right])

    const y = d3.scaleBand()
        .domain(d3.range(data.length))
        .rangeRound([margin.top, height - margin.bottom])
        .padding(0.1)

    const format = x.tickFormat(20, data.format)

    const xAxis = g => g
        .attr("transform", `translate(0,${margin.top})`)
        .call(d3.axisTop(x).ticks(width / 80, data.format))
        .call(g => g.select(".domain").remove())
        .attr("font-size", 10)

    const yAxis = g => g
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y).tickFormat(i => data[i].symbol).tickSizeOuter(0))
        .attr("font-size", 10)

    const svg = d3.select(svg_wrapper)
        .attr("viewBox", [0, 0, width, height]);

    // svg.append("text")
    //     .attr("x", (width / 2))
    //     .attr("y", margin.top / 2)
    //     .attr("text-anchor", "middle")
    //     .attr("font-family", "sans-serif")
    //     .style("font-size", "12px")
    //     .text(`Top ${numBar} ${type}`);

    svg.append("g")
        .attr("fill", fill)
        .selectAll("rect")
        .data(data)
        .join("rect")
        .attr("x", x(0))
        .attr("y", (d, i) => y(i))
        .attr("width", d => x(d.count) - x(0))
        .attr("height", y.bandwidth());

    svg.append("g")
        .attr("fill", "white")
        .attr("text-anchor", "end")
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
        .selectAll("text")
        .data(data)
        .join("text")
        .attr("x", d => x(d.count) - 4)
        .attr("y", (d, i) => y(i) + y.bandwidth() / 2)
        .attr("dy", "0.35em")
        .text(d => format(d.count));

    svg.append("g")
        .call(xAxis);

    svg.append("g")
        .call(yAxis);

    return svg.node();
}