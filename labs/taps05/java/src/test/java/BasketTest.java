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
import org.testng.annotations.Test;

public class BasketTest {
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

    @Test(groups = "smoke")
    public void twoCopiesGiveTheRightTotal() {
        driver.get(BASE + "/book.html?id=b1");
        driver.findElement(By.id("quantity")).clear();
        driver.findElement(By.id("quantity")).sendKeys("2");
        wait.until(ExpectedConditions.elementToBeClickable(By.id("add-button"))).click();
        driver.get(BASE + "/basket.html");
        wait.until(ExpectedConditions.textToBe(By.id("basket-total"), "Total: 36.00"));
        Assert.assertEquals(driver.findElements(By.cssSelector(".basket-line")).size(), 1);
        Assert.assertEquals(driver.findElement(By.id("basket-total")).getText(), "Total: 36.00");
    }
}
