<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>查询书籍</title>
    <link href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>

<div class="container">

    <div class="row clearfix">   <%--清除浮动 --%>
        <div class="col-md-12 column">
            <div class="page-header">
                <h1>
                    <small>书籍列表 ——— 显示所有书籍</small>
                </h1>
            </div>
        </div>

        <div class="row">
            <div class="col-md-4 column">
                <%--allBook--%>
                <a class="btn btn-primary" href="${pageContext.request.contextPath}/book/allBook">返回</a>
                <span style="color: red; font-weight:bold">${error}</span>    <%--如果未查找到该书籍，显示这一条--%>
            </div>
        </div>
    </div>

    <div class="row clearfix">
        <div class="col-md-12 column">
            <table class="table table-hover table-striped">
                <thead>
                <tr>
                    <th>书籍编号</th>
                    <th>书籍名称</th>
                    <th>书籍数量</th>
                    <th>书籍详情</th>
                    <th>操作</th>
                </tr>
                </thead>
                <c:forEach var="book" items="${list}">
                    <tr>
                        <td>${book.bookID}</td>
                        <td>${book.bookName}</td>
                        <td>${book.bookCounts}</td>
                        <td>${book.detail}</td>
                        <td>
                                <%--当点击修改的时候，接收 id, 跳转到BookController中的 toUpdata，再返回updata.jsp页面--%>
                            <a href="${pageContext.request.contextPath}/book/toUpdateBook?id=${book.bookID}">修改</a>
                            &nbsp;|&nbsp;   <%--空格--%>
                            <a href="${pageContext.request.contextPath}/book/deleteBook/${book.bookID}">删除</a>
                        </td>
                    </tr>
                </c:forEach>
                <tbody>

                </tbody>
            </table>
        </div>
    </div>
</div>

</body>
</html>
