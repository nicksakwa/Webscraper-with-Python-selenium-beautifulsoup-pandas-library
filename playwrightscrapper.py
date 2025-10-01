const { chromium } = require('playwright');
(async()=>{
    const browser = await chromium.launch{ headless: false}
    const page = await browser.newPage();
    await page.goto('https://toscrape.com/scroll');
    await page.mouse.wheel(0, 5000);
    await page.waitForSelector('.post-card', allPosts = >{
        return allPosts.map(post =>{
            const title =post.querySelector('.post-card-title a').textContent.trim();
            const author =post.querySelector('.post-card--author-name').textContent.trim();
            
            return {title, author};
        });
    });
    console.log('---Scraped Data---');
    console.log(posts);
    await browser.close();
})();