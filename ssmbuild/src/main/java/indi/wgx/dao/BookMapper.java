package indi.wgx.dao;

import indi.wgx.pojo.Books;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface BookMapper {

    // 增加一个 Book, 返回受影响的行数
    int addBook(Books book);

    // 根据 id 删除一个 Book
    int deleteBookById(@Param("bookID") int id);

    // 更新 Book
    int updateBook(Books book);

    // 根据 id 查询，返回一个 Book
    Books queryBookById(@Param("bookID") int id);

    // 查询全部 Book，返回list
    List<Books> queryAllBook();

    // 通过书籍名称查询
    Books queryBookByName(@Param("bookName") String bookName);
}
