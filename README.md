## ERPNext Point of Sale(POS) Coupon. [POC]

Provides a button within pos to apply coupons from within the Point of Sale in ERPNext. Coupons can be created from the native coupon functionality in ERPNext used for eCommerce at http://[your-erp-domain.com]/desk#List/Coupon%20Code/List

#### What works:
- Create coupon of any type. (Promotional or Gift Card)
- Apply a coupon in POS by clicking App Coupon. 
- Restrict coupon(gift card) to a single customer by linking a customer. 

#### Known limitations:
- Coupon only works in POS with offline mode enabled.
- Coupon limit settings is not fully implemented. Coupon can be used beyond allowed limit.
- Coupon currently only support Percentage Discount & Amount Discount in pricing rule linked to the coupon.

## Disclaimer:
This is a proof of concept. Don't use in production if you don't understand the code. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#### License

MIT
