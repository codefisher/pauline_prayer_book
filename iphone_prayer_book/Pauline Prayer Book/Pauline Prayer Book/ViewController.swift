//
//  ViewController.swift
//  Pauline Prayer Book
//
//  Created by Eremita on 25/04/17.
//
//

import UIKit
import AVFoundation
import WebKit

class ViewController: UIViewController, WKNavigationDelegate {
    
    //MARK: Properties
    @IBOutlet weak var webContentView: UIView!
    var webview: WKWebView?
    
    var player: AVMIDIPlayer?
    
    @IBOutlet weak var toolbar: UIToolbar!
    @IBOutlet weak var indexButton: UIBarButtonItem!
    @IBOutlet weak var topBar: UINavigationItem!
    
    var backBtn: UIBarButtonItem?
    
    let SegueMenuViewControler = "MenuViewControler"
    let SegueMenuItemTableViewController = "MenuItemTableViewController"

    override func viewDidLoad() {
        super.viewDidLoad()
        self.languageChanged()
        
        backBtn = UIBarButtonItem(title: "", style: UIBarButtonItem.Style.plain, target: self, action: #selector(self.goBack))
        if #available(iOS 13.0, *) {
            backBtn?.image = UIImage(systemName: "chevron.left")
        } else {
            backBtn?.title = NSLocalizedString("Back", comment: "")
        }
        
        #if targetEnvironment(macCatalyst)
        self.navigationItem.rightBarButtonItem = indexButton
        toolbar.isHidden = true
        #else
          //code to run on iOS
        #endif
    }
    
    func createWebView() {
        let configuration = WKWebViewConfiguration()
        configuration.setURLSchemeHandler(PrayerAssetHandler(), forURLScheme: "x-file")

        webview = WKWebView(frame: webContentView.bounds, configuration: configuration)
        self.webContentView.addSubview(webview!)
        webview?.autoresizingMask = webContentView.autoresizingMask
        webview?.frame = CGRect(x: 0, y: 0, width: webContentView.frame.width, height: webContentView.frame.height)
        webview!.navigationDelegate = self
    }
    
    @objc func goBack() {
        if((webview != nil) && webview!.canGoBack) {
            webview?.goBack()
        }
    }


    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        updateFontSize(webView: webview!)
    }
    
    func updateFontSize(webView: WKWebView) {
        let defaults = UserDefaults.standard //UserDefaults()
        var fontSize = defaults.string(forKey: "font_size")
        if fontSize == nil {
            fontSize = "14"
        }
        //print("document.body.style.fontSize = \"" + fontSize! + "px\";")
        webView.evaluateJavaScript("document.body.style.fontSize = \"" + fontSize! + "px\";")
        
        let currentTheme = defaults.integer(forKey: "theme_type")
        if(currentTheme == 1) {
            webView.evaluateJavaScript("document.body.classList.add(\"darktheme\")")
        }
    }
    
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        if(webView.canGoBack) {
             self.navigationItem.hidesBackButton = false
             self.navigationItem.leftBarButtonItem = backBtn
        } else {
            self.navigationItem.hidesBackButton = true
            self.navigationItem.leftBarButtonItem = nil
        }
        webView.evaluateJavaScript("window.scrollTo(0,0)", completionHandler: nil)
        updateFontSize(webView: webView)
    }
    
    func webView(_ webView: WKWebView, decidePolicyFor navigationAction: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
        //print("WebView opening:" + request.url!.absoluteString + " with scheme:" + request.url!.scheme!)
        let request = navigationAction.request
        if(request.url!.scheme == "mailto" || request.url!.scheme == "http") {
            UIApplication.shared.open(request.url!, options: [:], completionHandler: nil)
            decisionHandler(.cancel)
            return;
        } else if(request.url!.scheme == "musicplay") {
            // for some reason request.url!.path is always empty???
            let filename = request.url!.host
            if(filename == "" || filename == nil) {
                if(player != nil) {
                    player?.stop()
                }
            } else {
                let url = Bundle.main.url(forResource: "raw/" + filename!, withExtension: "mid")
                let sounds = Bundle.main.url(forResource: "jeux14", withExtension: "sf2")
                if(url == nil) {
                    decisionHandler(.cancel)
                    return
                }
                do {
                    player = try AVMIDIPlayer(contentsOf: url!, soundBankURL: sounds!)
                    guard let player = player else { decisionHandler(.cancel); return  }
                    
                    player.prepareToPlay()
                    player.play(nil)
                } catch let error as NSError {
                    NSLog("Music Play Error")
                    NSLog(error.description)
                }
            }
            decisionHandler(.cancel)
        }
        decisionHandler(.allow)
    }
    
    func languageChanged() {
        self.webview?.removeFromSuperview()
        self.createWebView()
        loadPage(page: "front")
    }
    
    func loadPage(page: String) {
        let defaults = UserDefaults.standard //UserDefaults()
        
        var language = defaults.string(forKey: "prayer_language")
        if language == nil {
            language = NSLocalizedString("default_locale", comment: "")
        }
        
        var htmlFile = Bundle.main.url(forResource: "prayers/" + language! + "/" + page, withExtension: "html" )
        var xHtmlFile = URL(string: "x-file:///" + language! + "/" + page + ".html")
        //let html = try? String(contentsOfFile: htmlFile!, encoding: NSUTF8StringEncoding)
        if(htmlFile == nil) {
            htmlFile = Bundle.main.url(forResource: "prayers/" + language! + "/front", withExtension: "html" )
            xHtmlFile = URL(string: "x-file:///" + language! + "/front.html")
        }
        
        let url = URLRequest(url: xHtmlFile!)
        webview!.load(url)
    }
    
    func reload() {
        guard let urlCheck = webview?.url
            else {return}
        let url = URLRequest(url: urlCheck)
        webview!.load(url)
    }
    
    @objc func printPage() {
        guard let urlCheck = webview?.url
            else {return}
        
        let pi = UIPrintInfo.printInfo()
        pi.outputType = .general
        pi.jobName = urlCheck.absoluteString
        pi.orientation = .portrait
        pi.duplex = .longEdge

        let printController = UIPrintInteractionController.shared
        printController.printInfo = pi
        printController.printFormatter = webview?.viewPrintFormatter()
        printController.present(animated: true, completionHandler: nil)
    }
    
    @objc func openAbout() {
        self.loadPage(page: "about")
    }
    
    @objc func goSettings() {
        self.performSegue(withIdentifier: self.SegueMenuViewControler, sender: self)
    }

    //MARK: Actions

    @IBAction func indexButton(_ sender: UIBarButtonItem) {
        #if targetEnvironment(macCatalyst)
        for aView in view.subviews {
            if let ctl = aView as? UITableView {
                // we found the menu view remove it and stop
                ctl.removeFromSuperview()
                return
            }
        }
        let controller = storyboard!.instantiateViewController(withIdentifier: "indexView")
        addChild(controller)
        let frame = webview?.frame
        controller.view.frame = CGRect(x: frame!.width - 350, y: 0, width: 350, height: frame!.height);
        view.addSubview(controller.view)
        controller.didMove(toParent: self)
        #else
          performSegue(withIdentifier: SegueMenuItemTableViewController, sender: self)
        #endif
    }
    
    @IBAction func menuButton(_ sender: UIBarButtonItem) {
        let optionMenu = UIAlertController(title: nil, message: nil, preferredStyle: .actionSheet)

        let settingsAction = UIAlertAction(title: NSLocalizedString("Settings", comment: ""), style: .default, handler:
        {
            (alert: UIAlertAction!) -> Void in
            self.goSettings()
        })

        let aboutAction = UIAlertAction(title: NSLocalizedString("About", comment: ""), style: .default, handler:
        {
            (alert: UIAlertAction!) -> Void in
            self.openAbout()
        })
        
        let printAction = UIAlertAction(title: NSLocalizedString("Print", comment: ""), style: .default, handler:
        {
            (alert: UIAlertAction!) -> Void in
            self.printPage()
        })
        
        let cancelAction = UIAlertAction(title: NSLocalizedString("Cancel", comment: ""), style: .cancel, handler:
        {
            (alert: UIAlertAction!) -> Void in
        })
        
        optionMenu.addAction(settingsAction)
        optionMenu.addAction(aboutAction)
        optionMenu.addAction(printAction)
        optionMenu.addAction(cancelAction)
        self.present(optionMenu, animated: true, completion: nil)
    }
    
    

}
