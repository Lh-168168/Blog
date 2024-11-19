var newsearchFunc = function (path, search_id, content_id) {
    //'use strict';
    $.ajax({
        url: path,
        dataType: "json",
        success: function (datas) {
            // get the contents from search data
            // var datas = $("entry", xmlResponse).map(function () {
            //     return {
            //         title: $("title", this).text(),
            //         content: $("content", this).text(),
            //         url: $("url", this).text()
            //     };
            // }).get();
            var $input = document.getElementById(search_id);
            var $resultContent = document.getElementById(content_id);
            $input.addEventListener('input', function () {
                var str = '<ul class=\"search-result-list\">';
                var keywords = this.value.trim().toLowerCase().split(/[\s\-]+/);
                $resultContent.innerHTML = "";
                if (this.value.trim().length <= 0) {
                    return;
                }
                // perform local searching
                datas.forEach(function (data) {
                    var isMatch = true;
                    var content_index = [];
                    var data_title = data.title.trim().toLowerCase();
                    var data_content = data.content.trim().replace(/<[^>]+>/g, "").toLowerCase();
                    var data_url = data.url;
                    var index_title = -1;
                    var index_content = -1;
                    var first_occur = -1;
                    // only match artiles with not empty titles and contents
                    if (data_title != '' && data_content != '') {
                        keywords.forEach(function (keyword, i) {
                            index_title = data_title.indexOf(keyword);
                            index_content = data_content.indexOf(keyword);
                            if (index_title < 0 && index_content < 0) {
                                isMatch = false;
                            } else {
                                if (index_content < 0) {
                                    index_content = 0;
                                }
                                if (i == 0) {
                                    first_occur = index_content;
                                }
                            }
                        });
                    }
                    // show search results
                    // if (isMatch) {
                    //     str += "<li><a href='" + data_url + "' class='search-result-title'>" + data_title + "</a>";
                    //     var content = data.content.trim().replace(/<[^>]+>/g, "");
                    //     if (first_occur >= 0) {
                    //         // cut out 100 characters
                    //         var start = first_occur - 20;
                    //         var end = first_occur + 80;
                    //         if (start < 0) {
                    //             start = 0;
                    //         }
                    //         if (start == 0) {
                    //             end = 100;
                    //         }
                    //         if (end > content.length) {
                    //             end = content.length;
                    //         }
                    //         var match_content = content.substr(start, end);
                    //         // highlight all keywords
                    //         keywords.forEach(function (keyword) {
                    //             var regS = new RegExp(keyword, "gi");
                    //             match_content = match_content.replace(regS, "<em class=\"search-keyword\">" + keyword + "</em>");
                    //         });

                    //         str += "<p class=\"search-result\">" + match_content + "...</p>"
                    //     }
                    //     str += "</li>";
                    // }
                    if (isMatch) {
                        str += "<li><a href='" + data_url + "' class='search-result-title'>" + data_title + "</a>";
                        // var content = data.content.trim().replace(/<[^>]+>/g, "");
                        var content = data.content.trim();

                        // 鍘婚櫎 HTML 鏍囩鍜� Markdown 绗﹀彿
                        content = content.replace(/<[^>]+>/g, ''); // 鍘婚櫎 HTML 鏍囩
                        if (first_occur >= 0) {
                            // 鎴彇鎼滅储鍏抽敭璇嶅墠鍚庡悇20涓瓧绗︾殑鍐呭
                            var start = Math.max(0, first_occur - 50); // 纭繚涓嶄細瓒呭嚭瀛楃涓插紑澶�
                            var end = first_occur + 50; // 纭畾缁撴潫浣嶇疆

                            // 濡傛灉缁撴潫浣嶇疆瓒呭嚭浜嗗瓧绗︿覆鐨勬湯灏撅紝鍒欒繘琛岃皟鏁�
                            if (end > content.length) {
                                end = content.length;
                            }

                            var match_content = content.substring(start, end); // 鑾峰彇鎴彇鐨勫唴瀹圭墖娈�

                            // 鍏抽敭璇嶉珮浜�
                            var keyword = keywords[0]; // 鍋囪鍙鐞嗗崟涓叧閿瘝鐨勬儏鍐�
                            var regS = new RegExp(keyword, "gi");
                            match_content = match_content.replace(regS, "<em class=\"search-keyword\">" + keyword + "</em>");

                            str += "<p class=\"search-result\">" + match_content + "...</p>";
                        }
                        str += "</li>";
                    }
                });
                str += "</ul>";
                $resultContent.innerHTML = str;
            });
        }
    });
}