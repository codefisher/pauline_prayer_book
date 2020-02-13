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
    @IBOutlet weak var webview: WKWebView!
    
    var player: AVMIDIPlayer?
    
    let SegueMenuViewControler = "MenuViewControler"
    let SegueMenuItemTableViewController = "MenuItemTableViewController"

    override func viewDidLoad() {
        super.viewDidLoad()
        webview.navigationDelegate = self
        // Do any additional setup after loading the view, typically from a nib.        
        self.languageChanged()
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        updateFontSize(webView: webview)
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
        loadPage(page: "front")
    }
    
    func loadPage(page: String) {
        let defaults = UserDefaults.standard //UserDefaults()
        
        var language = defaults.string(forKey: "prayer_language")
        if language == nil {
            language = NSLocalizedString("default_locale", comment: "")
        }
        
        var htmlFile = Bundle.main.url(forResource: "prayers/" + language! + "/" + page, withExtension: "html" )
        //let html = try? String(contentsOfFile: htmlFile!, encoding: NSUTF8StringEncoding)
        if(htmlFile == nil) {
            htmlFile = Bundle.main.url(forResource: "prayers/" + language! + "/front", withExtension: "html" )
        }
        let url = URLRequest(url: htmlFile!)
        webview.load(url)
    }

    //MARK: Actions

    @IBAction func indexButton(_ sender: UIBarButtonItem) {
        performSegue(withIdentifier: SegueMenuItemTableViewController, sender: self)
    }
    
    @IBAction func menuButton(_ sender: UIBarButtonItem) {
        performSegue(withIdentifier: SegueMenuViewControler, sender: self)
    }
    
    

}
