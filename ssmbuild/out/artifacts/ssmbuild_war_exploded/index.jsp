<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>首页</title>

    <%--<style> 标签用于为 HTML 文档定义样式信息。在 style 中，可以规定在浏览器中如何呈现 HTML 文档--%>
    <style>
        a{
            text-decoration: none;  /*去掉文字下面的横线*/
            color: #000000;  /*定义文字的颜色*/
            font-size: 18px;  /*字体大小*/
        }
        h3{
            width: 180px;
            height: 38px;
            margin: 100px auto;  /*外边距*/
            text-align: center;  /*文本居中*/
            line-height: 38px;  /*行高*/
            background: deepskyblue;  /*背景颜色*/
            border-radius: 5px;  /*圆角边框*/
        }

    </style>



</head>
<body>


<h3>
    <%--取绝对地址--%>
    <a href="${pageContext.request.contextPath}/book/allBook">登录</a>
</h3>
</body>
</html>
