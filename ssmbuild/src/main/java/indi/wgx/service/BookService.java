package indi.wgx.service;

import indi.wgx.pojo.Books;
import org.apache.ibatis.annotations.Param;

import java.util.List;

// 业务层
public interface BookService {
    // 增加一个 Book, 返回受影响的行数
    int addBook(Books book);

    // 根据 id 删除一个 Book
    // 在方法参数的前面写上@Param("参数名"),表示给参数命名,名称就是括号中的内容
    int deleteBookById(int id);

    // 更新 Book
    int updateBook(Books book);

    // 根据 id 查询，返回一个 Book
    Books queryBookById(int id);

    // 查询全部 Book，返回list
    List<Books> queryAllBook();

    // 通过书籍名称查询
    Books queryBookByName(String bookName);

}
