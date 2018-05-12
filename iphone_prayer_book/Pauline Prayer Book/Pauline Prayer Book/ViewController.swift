//
//  ViewController.swift
//  Pauline Prayer Book
//
//  Created by Eremita on 25/04/17.
//
//

import UIKit
import AVFoundation

class ViewController: UIViewController, UIWebViewDelegate {
    
    //MARK: Properties
    @IBOutlet weak var webview: UIWebView!
    
    var player: AVMIDIPlayer?
    
    let SegueMenuViewControler = "MenuViewControler"
    let SegueMenuItemTableViewController = "MenuItemTableViewController"

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
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        updateFontSize(webView: webview)
    }
    
    func updateFontSize(webView: UIWebView) {
        let defaults = UserDefaults.standard //UserDefaults()
        var fontSize = defaults.string(forKey: "font_size")
        if fontSize == nil {
            fontSize = "14"
        }
        webView.stringByEvaluatingJavaScript(from: "document.body.style.fontSize = \"" + fontSize! + "px\"")
    }
    
    func webViewDidFinishLoad(_ webView: UIWebView) {
        updateFontSize(webView: webView)
    }
    
    func webView(_ webView: UIWebView, shouldStartLoadWith request: URLRequest, navigationType: UIWebViewNavigationType) -> Bool {
        if(request.url!.scheme == "mailto" || request.url!.scheme == "http") {
            UIApplication.shared.open(request.url!, options: [:], completionHandler: nil)
            return false;
        } else if(request.url!.scheme == "musicplay") {
            if(request.url!.path == "") {
                if(player != nil) {
                    player?.stop()
                }
            } else {
                let url = Bundle.main.url(forResource: "raw/" + request.url!.path, withExtension: "mid")
                let sounds = Bundle.main.url(forResource: "jeux14", withExtension: "sf2")
                if(url == nil) {
                    return false
                }
                do {
                    player = try AVMIDIPlayer(contentsOf: url!, soundBankURL: sounds!)
                    guard let player = player else { return false }
                    
                    player.prepareToPlay()
                    player.play(nil)
                } catch let error as NSError {
                    print(error.description)
                }
            }
            return false;
        }
        return true
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
        webview.loadRequest(url)
    }

    //MARK: Actions

    @IBAction func indexButton(_ sender: UIBarButtonItem) {
        performSegue(withIdentifier: SegueMenuItemTableViewController, sender: self)
    }
    
    @IBAction func menuButton(_ sender: UIBarButtonItem) {
        performSegue(withIdentifier: SegueMenuViewControler, sender: self)
    }
    
    

}

