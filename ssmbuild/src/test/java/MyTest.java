import indi.wgx.pojo.Books;
import indi.wgx.service.BookService;
import org.junit.Test;
import org.springframework.context.support.ClassPathXmlApplicationContext;

// 单元测试
public class MyTest {
    @Test
    public void test(){
        ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext("applicationContext.xml");// 拿到所有的bean
        BookService bookServiceImpl = (BookService) context.getBean("bookServiceImpl");
        for(Books books : bookServiceImpl.queryAllBook()){
            System.out.println(books);
        }
    }
}
