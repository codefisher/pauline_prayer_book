//
//  ViewController.swift
//  Pauline Prayer Book
//
//  Created by Eremita on 25/04/17.
//
//

import UIKit

class ViewController: UIViewController {
    
    //MARK: Properties
    @IBOutlet weak var webview: UIWebView!

    
    @IBOutlet weak var indexButton: UIBarButtonItem!

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        print("loading")
        
        //indexButton.target = self
        //indexButton.action = #selector(indexAction)
        
        let htmlFile = NSBundle.mainBundle().URLForResource("prayers/pl/front", withExtension: "html" )
        //let html = try? String(contentsOfFile: htmlFile!, encoding: NSUTF8StringEncoding)
        let url = NSURLRequest(URL: htmlFile!)
        webview.loadRequest(url)
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    //MARK: Actions
    
    @IBAction func indexAction(sender: UIBarButtonItem) {
  
        let viewController: ViewController = self.storyboard?.instantiateViewControllerWithIdentifier("indexView") as! ViewController
        self.presentViewController(viewController, animated: true, completion: nil)
    }
    
    

    @IBAction func menuButton(sender: UIBarButtonItem) {
    }


}

