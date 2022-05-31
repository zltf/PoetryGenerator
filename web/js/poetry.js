// 生成诗词
// brand_name：词牌名
function gen_poetry(sentence, position, line_len){
    // 调用生成诗词的api接口
    $.get("http://zhiskey.cn:5000/generate_tang_by_structure_hide_sentence?sentence=" + sentence + "&position=" + position + "&line_len=" + line_len, function(result){
        result = JSON.parse(result);
        html = "";
        // 将生成的诗词显示在前端界面中
        for (i in result){
            html += "<li class=\"list-group-item\">" + result[i] + "</li>";
        }
        $(".list-group").html(html);
    });
}
