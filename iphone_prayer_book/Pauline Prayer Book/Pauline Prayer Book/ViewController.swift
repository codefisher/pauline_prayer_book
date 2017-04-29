//
//  ViewController.swift
//  Pauline Prayer Book
//
//  Created by Eremita on 25/04/17.
//
//

import UIKit

class ViewController: UIViewController, UIWebViewDelegate {
    
    //MARK: Properties
    @IBOutlet weak var webview: UIWebView!
    
    let SegueMenuViewControler = "MenuViewControler"
    let SegueMenuItemTableViewController = "MenuItemTableViewController"

    
    @IBOutlet weak var indexButton: UIBarButtonItem!

    override func viewDidLoad() {
        super.viewDidLoad()
        webview.delegate = self
        // Do any additional setup after loading the view, typically from a nib.        
        self.languageChanged()
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        updateFontSize(webview)
    }
    
    func updateFontSize(webView: UIWebView) {
        let defaults = NSUserDefaults.standardUserDefaults()
        var fontSize = defaults.stringForKey("font_size")
        if fontSize == nil {
            fontSize = "14"
        }
        webView.stringByEvaluatingJavaScriptFromString("document.body.style.fontSize = \"" + fontSize! + "px\"")
    }
    
    func webViewDidFinishLoad(webView: UIWebView) {
        updateFontSize(webView)
    }
    
    func webView(webView: UIWebView, shouldStartLoadWithRequest request: NSURLRequest, navigationType: UIWebViewNavigationType) -> Bool {
        if(request.URL!.scheme == "mailto" || request.URL!.scheme == "http") {
            UIApplication.sharedApplication().openURL(request.URL!)
            return false;
        }
        return true
    }
    
    func languageChanged() {
        loadPage("front")
    }
    
    func loadPage(page: String) {
        let defaults = NSUserDefaults.standardUserDefaults()
        
        var language = defaults.stringForKey("prayer_language")
        if language == nil {
            language = NSLocalizedString("default_locale", comment: "")
        }
        
        var htmlFile = NSBundle.mainBundle().URLForResource("prayers/" + language! + "/" + page, withExtension: "html" )
        //let html = try? String(contentsOfFile: htmlFile!, encoding: NSUTF8StringEncoding)
        if(htmlFile == nil) {
            htmlFile = NSBundle.mainBundle().URLForResource("prayers/" + language! + "/front", withExtension: "html" )
        }
        let url = NSURLRequest(URL: htmlFile!)
        webview.loadRequest(url)
    }

    //MARK: Actions
    
    @IBAction func indexAction(sender: UIBarButtonItem) {
        performSegueWithIdentifier(SegueMenuItemTableViewController, sender: self)

    }
    
    @IBAction func menuButton(sender: UIBarButtonItem) {
        performSegueWithIdentifier(SegueMenuViewControler, sender: self)
    }
    


}

