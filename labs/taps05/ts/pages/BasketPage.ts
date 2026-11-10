import { Locator, Page } from '@playwright/test';

export class BasketPage {
  readonly lines: Locator;
  readonly total: Locator;

  constructor(private readonly page: Page) {
    this.lines = page.locator('.basket-line');
    this.total = page.getByTestId('basket-total');
  }

  async open(): Promise<void> {
    await this.page.goto('/basket.html');
  }
}
