function chart(data, svg_wrapper, numBar) {

    data = data.sort((a, b) => d3.descending(a.count, b.count)).slice(0, numBar);
    const margin = ({top: 90, right: 30, bottom: 10, left: 100})
    const barHeight = 25
    const width = 600;
    const height = Math.ceil((data.length + 0.1) * barHeight) + margin.top + margin.bottom

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
        .attr("font-size", 14)

    const yAxis = g => g
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y).tickFormat(i => data[i].symbol).tickSizeOuter(0))
        .attr("font-size", 14)

    const svg = d3.select(svg_wrapper)
        .attr("viewBox", [0, 0, width, height]);

    svg.append("text")
        .attr("x", (width / 2))
        .attr("y", margin.top / 2)
        .attr("text-anchor", "middle")
        .attr("font-family", "sans-serif")
        .style("font-size", "16px")
        .text(`Top ${numBar} drugs`);

    svg.append("g")
        .attr("fill", "#9a9a9a")
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
        .attr("font-size", 14)
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