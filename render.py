def render(jsontext):
    return """<html>

<head>
    <meta charset="utf-8" />
    <link href="https://fonts.googleapis.com/css2?family=Jua&display=swap" rel="stylesheet">
</head>
<style>
    .link  {
    stroke: #999;
    stroke-opacity: 0.6;
    }

    .nodes circle {
    stroke: #fff;
    stroke-width: 1.5px;
    }

    .outline {
    outline: 6px solid black;
    outline-style:dashed;
    }
    .outline-nondash {
    outline: 6px solid black;
    outline-style:auto;
    }
    .small {
        font-size: 15px;
        font-family:Arial, Helvetica, sans-serif;
    }
</style>

<body>
    <div class="wordcloud">
        <h1 font-family='san-serif'>Word Cloud</h1>
    </div>
    <div class="cooccur">
        <h1 font-family='san-serif'>Cooccurence Detail</h1>
    </div>
    <h1 class="small">문장내에서 자주 같이 출연하는 단어들의 상위 10개 단어의 네트워크입니다.</h1>
    <div class="similar">
        <h1 font-family='san-serif'>Similar Detail</h1>
    </div>
    <h1 class="small">문장 등장 위치에 따른 유사하다고 생각되는 단어 top 10의 네트워크입니다..</h1>
    <script src="https://d3js.org/d3.v3.min.js"></script>
    <script src="https://rawgit.com/jasondavies/d3-cloud/master/build/d3.layout.cloud.js" type="text/JavaScript">
    </script>
    <script>
        var dataAnalyze = """ + jsontext + """
        var width = 1300,
            height = 600

        var svg = d3.select(".wordcloud").append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("class", 'outline');

        var svg = d3.select("svg")
            .append("g")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")

        showCloud(dataAnalyze)


        function showCloud(data) {
            d3.layout.cloud().size([width, height])
                //클라우드 레이아웃에 데이터 전달
                .words(data.map((d, index) => {
                    return {
                        index: index,
                        text: d.keyword,
                        size: d.score,
                        cooccur: d.cooccur,
                        similar: d.similar,
                    }
                }))
                .padding(30)
                //스케일로 각 단어의 크기를 설정
                .rotate(function (d) {
                    return Math.round((Math.random()-0.5)*2) * 90;
                })
                .fontSize(d => {
                    if (d.index < 10) {
                        return 60;
                    } else {
                        return 30;
                    }
                })
                .on("end", draw)
                .start();

            function draw(words) {
                var cloud = svg.selectAll("text").data(words)
                //Entering words
                cloud.enter()
                    .append("text")
                    .style("font-family", 'Jua')
                    .style("fill", function (d) {
                        return (d.index < 10 ? "#fbc280" : "#405275");
                    })
                    .style("fill-opacity", .5)
                    .attr("text-anchor", "center")
                    .text(function (d) {
                        return d.text;
                    })
                    .on('click', overevent)
                cloud.transition()
                    .duration(600)
                    .style("font-size", function (d) {
                        return d.size + "px";
                    })
                    .attr("transform", function (d) {
                        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                    })
                    .style("fill-opacity", 1);
            }


            function overevent(d) {
                showdetail(d);
                similardetail(d);
            }
        }
        function showdetail(d) {
            var width = 400,
                height = 400;
            var central = d.text;
            var links = d.cooccur.map((d) => {
                return {
                    "source": central,
                    "target": d.subkeyword,
                    "value": d.cooccur_num
                }
            });
            var nodes = {};
            linkScale = d3.scale.linear().domain([0, links[0].value]).range([0, 150]).clamp(true);

            console.log(links)
            // Compute the distinct nodes from the links.
            links.forEach(function (link) {
                link.source = nodes[link.source] || (nodes[link.source] = {
                    name: link.source

                });
                link.target = nodes[link.target] || (nodes[link.target] = {
                    name: link.target
                });
                
            });


            var force = d3.layout.force()
                .nodes(d3.values(nodes))
                .links(links)
                .size([width, height])
                .linkDistance((link)=>{
                    return linkScale(link.value)
                })
                .charge(-300)
                .on("tick", tick)
                .start();

            var svg = d3.select(".cooccur").append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("class",'outline');

            var link = svg.selectAll(".link")
                .data(force.links())
                .enter().append("line")
                .attr("class", "link")


            var color = d3.scale.category20();

            var node = svg.selectAll(".node")
                .data(force.nodes())
                .enter().append("g")
                .attr("class", "node")
                .on("mouseover", mouseover)
                .on("mouseout", mouseout)
                .call(force.drag);


            node.append("circle")
                .attr("r", 8)
                .attr("fill", function(d,i){return color(i);});


            node.append("text")
                .attr("x", 12)
                .attr("dy", ".35em")
                .text(function (d) {
                    return d.name;
                });

            function tick() {
                link
                    .attr("x1", function (d) {
                        return d.source.x;
                    })
                    .attr("y1", function (d) {
                        return d.source.y;
                    })
                    .attr("x2", function (d) {
                        return d.target.x;
                    })
                    .attr("y2", function (d) {
                        return d.target.y;
                    });

                node
                    .attr("transform", function (d) {
                        return "translate(" + d.x + "," + d.y + ")";
                    });
            }

            function mouseover() {
                d3.select(this).select("circle").transition()
                    .duration(750)
                    .attr("r", 16);
            }

            function mouseout() {
                d3.select(this).select("circle").transition()
                    .duration(750)
                    .attr("r", 8);
            }
        }
    </script>
       <script>
           function similardetail(d) {
               var width = 400,
                   height = 400;
               var central = d.text;
               console.log(d)
               var links = d.similar.map((d) => {
                   return {
                       "source": central,
                       "target": d.subkeyword,
                       "value": d.cooccur_num
                   }
               });
               var nodes = {};
               linkScale = d3.scale.linear().domain([0, 1]).range([0, 100]).clamp(true);
   
               // Compute the distinct nodes from the links.
               links.forEach(function (link) {
                   link.source = nodes[link.source] || (nodes[link.source] = {
                       name: link.source
   
                   });
                   link.target = nodes[link.target] || (nodes[link.target] = {
                       name: link.target
                   });
                   
               });
   
   
               var force = d3.layout.force()
                   .nodes(d3.values(nodes))
                   .links(links)
                   .size([width, height])
                   .linkDistance((link)=>{
                       return linkScale(link.value)
                   })
                   .charge(-300)
                   .on("tick", tick)
                   .start();
   
               var svg = d3.select(".similar").append("svg")
                   .attr("width", width)
                   .attr("height", height)
                   .attr("class",'outline');
   
               var link = svg.selectAll(".link")
                   .data(force.links())
                   .enter().append("line")
                   .attr("class", "link");
   
               var color = d3.scale.category20();
   
               var node = svg.selectAll(".node")
                   .data(force.nodes())
                   .enter().append("g")
                   .attr("class", "node")
                   .on("mouseover", mouseover)
                   .on("mouseout", mouseout)
                   .call(force.drag);
   
               node.append("circle")
                   .attr("r", 8)
                   .attr("fill", (d,i)=>color(i));
   
   
               node.append("text")
                   .attr("x", 12)
                   .attr("dy", ".35em")
                   .text(function (d) {
                       return d.name;
                   });
   
               function tick() {
                   link
                       .attr("x1", function (d) {
                           return d.source.x;
                       })
                       .attr("y1", function (d) {
                           return d.source.y;
                       })
                       .attr("x2", function (d) {
                           return d.target.x;
                       })
                       .attr("y2", function (d) {
                           return d.target.y;
                       });
   
                   node
                       .attr("transform", function (d) {
                           return "translate(" + d.x + "," + d.y + ")";
                       });
               }
   
               function mouseover() {
                   d3.select(this).select("circle").transition()
                       .duration(750)
                       .attr("r", 16);
               }
   
               function mouseout() {
                   d3.select(this).select("circle").transition()
                       .duration(750)
                       .attr("r", 8);
               }
           }
        </script>

</body>

</html>"""
