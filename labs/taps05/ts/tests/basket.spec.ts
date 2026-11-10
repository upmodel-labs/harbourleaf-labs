import { test, expect, Page } from '@playwright/test';
import { BasketPage } from '../pages/BasketPage';

const bookId: string = 'b1';
const copies: number = 2;

async function addBook(page: Page, id: string, quantity: number): Promise<void> {
  await page.goto(`/book.html?id=${id}`);
  await page.getByLabel('Quantity').fill(String(quantity));
  await page.getByRole('button', { name: 'Add to basket' }).click();
}

test('two copies give the right total @smoke', async ({ page }) => {
  const basket = new BasketPage(page);
  await addBook(page, bookId, copies);
  await basket.open();
  await expect(basket.lines).toHaveCount(1);
  await expect(basket.total).toHaveText('Total: 36.00');
});
