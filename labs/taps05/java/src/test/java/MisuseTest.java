import java.time.Duration;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

/** Step 6, Attack logs track. Run it only against the practice shop you started yourself. */
public class MisuseTest {
    private static final String BASE = "http://localhost:8000";

    private WebDriver driver;
    private WebDriverWait wait;

    @BeforeMethod(alwaysRun = true)
    public void startBrowser() {
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--window-size=1280,900");
        driver = new ChromeDriver(options);
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    @AfterMethod(alwaysRun = true)
    public void stopBrowser() {
        if (driver != null) {
            driver.quit();
        }
    }

    /** Does the reply area of the help box show this text? It looks only at #help-reply. */
    private boolean replyShowsText(String text) {
        return driver.findElement(By.cssSelector("#help-reply")).getText().contains(text);
    }

    /** Does the page have an element that matches this CSS selector? */
    private boolean pageHasElement(String cssSelector) {
        return !driver.findElements(By.cssSelector(cssSelector)).isEmpty();
    }

    /** Rows are (input, kind, value). Kind "text": the reply must never show value. Kind "element": the page must never have an element matching value. */
    @DataProvider(name = "misuse")
    public Object[][] misuse() {
        return new Object[][] {
            {"", "", ""},                                  // row 1: the other customer's order number (you fill this in)
            {"", "", ""},                                  // row 2: the HTML snippet (you fill this in)
            {"X".repeat(200), "text", "X".repeat(41)},     // row 3: a very long string (done for you): the reply repeats only 40 characters
        };
    }

    @Test(dataProvider = "misuse", groups = "misuse")
    public void misuseInputIsHandled(String input, String kind, String value) {
        driver.get(BASE + "/help.html");
        driver.findElement(By.cssSelector("[data-testid='order-box']")).sendKeys(input);
        driver.findElement(By.cssSelector("[data-testid='ask-button']")).click();
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector("#help-reply.is-ready")));

        if (kind.equals("text")) {
            // TODO: assert that the reply never shows value. Use replyShowsText.
        } else if (kind.equals("element")) {
            // TODO: assert that the page never has an element that matches value. Use pageHasElement.
        }
    }
}
