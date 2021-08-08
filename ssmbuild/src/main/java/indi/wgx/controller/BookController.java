package indi.wgx.controller;

import indi.wgx.pojo.Books;
import indi.wgx.service.BookService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.ArrayList;
import java.util.List;

@Controller
@RequestMapping("/book")
public class BookController {

    // controller 调用 service 层
    @Autowired
    @Qualifier("bookServiceImpl")
    private BookService bookService;

    // 查询全部的书籍，并且返回到一个书籍展示页面
    @RequestMapping("/allBook")
    public String list(Model model){
        List<Books> list = bookService.queryAllBook();
        // 返回给前端去展示
        model.addAttribute("list", list);
        return "allBook";
    }

    // 跳转到增加书籍页面
    @RequestMapping("/toAddBook")
    public String toAddPage(){
        return "addBook";  // 跳转到 addBook.jsp
    }

    // 添加书籍的请求
    @RequestMapping("/addBook")
    public String addBook(Books books){
        System.out.println(books);
        bookService.addBook(books);
        return "redirect:/book/allBook";  // 重定向到 @RequestMapping("/allBook") 这个请求
    }

    // 跳转到修改书籍信息的页面
    @RequestMapping("/toUpdateBook")
    public String toUpdateBook(Model model, int id) {
        Books books = bookService.queryBookById(id);  // 通过id查询到这本书
        System.out.println("即将要修改的书籍信息：" + books);  // 打印出要修改的书籍信息
        model.addAttribute("book",books );  // 带给前端
        return "updateBook";
    }

    @RequestMapping("/updateBook")
    public String updateBook(Model model, Books book) {
        System.out.println("将书籍信息修改为：" + book);  // 输出修改了哪本书
        bookService.updateBook(book);  // 调用业务层修改
        Books books = bookService.queryBookById(book.getBookID());  // 通过id查找并返回修改后的书籍
        model.addAttribute("books", books);  // 将修改后的书籍返回到前端
        return "redirect:/book/allBook";  // allBook.jsp
    }

    // 删除书籍
    @RequestMapping("/deleteBook/{bookID}")
    public String deleteBook(@PathVariable("bookID") int id){
        bookService.deleteBookById(id);
        return "redirect:/book/allBook";
    }

    // 查询书籍
    @RequestMapping("/queryBook")
    public String queryBook(String queryBookName, Model model){
        Books books = bookService.queryBookByName(queryBookName);  // 查询出来的书籍命名为 books
        List<Books> list = new ArrayList<>();  // 创建list集合，这里其实也可以在 BookMapper接口直接改成 list集合接收
        list.add(books);
        if(books == null){
            model.addAttribute("error", "未找到此书籍");
        }
        System.out.println(list);
        model.addAttribute("list", list);
        return "queryBook";   // 跳转到 queryBook.jsp 页面
    }
}
