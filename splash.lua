function main(splash, args)
    assert(splash:go(args.url))

    while not splash:select('#beerName')
            and not splash:select("#root > div > div:nth-child(2) > div > div:nth-child(2) > div > div:nth-child(1) > span")
            and not splash:select("#root > div > div:nth-child(2) > div > h2 > span") do
        assert(splash:wait(0.1))
    end

    if splash:select("#root > div > div:nth-child(2) > div > div:nth-child(2) > div > div:nth-child(1) > span")
            or splash:select("#root > div > div:nth-child(2) > div > h2 > span") then
        return {
            html = splash:html()
        }
    end

    while splash:select('#beerName'):text() == 'Loading...' do
        assert(splash:wait(0.1))
    end

    return {
        html = splash:html()
    }
end