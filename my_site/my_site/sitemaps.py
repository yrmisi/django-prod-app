from blogapp.sitemap import BlogSitemap
from myauth.sitemap import ProfileSitemap
from shop_app.sitemap import ShopSitemap

sitemaps: dict[str, BlogSitemap | ShopSitemap | ProfileSitemap] = {
    "blog": BlogSitemap,
    "shop": ShopSitemap,
    "profile": ProfileSitemap,
}
