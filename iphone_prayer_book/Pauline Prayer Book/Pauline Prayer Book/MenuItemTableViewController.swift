//
//  MenuItemTableViewController.swift
//  Pauline Prayer Book
//
//  Created by Eremita on 25/04/17.
//
//

import UIKit

class MenuItemTableViewController: UITableViewController, NSXMLParserDelegate {
    
    var parser = NSXMLParser()
    
    class MenuItem {
        var title: String = ""
        var doc: String = ""
        var children: [AnyObject] = [AnyObject]()
        
        init(aTitle: String, aDoc: String) {
            title = aTitle
            doc = aDoc
        }
        
        init(aTitle: String, aChildren: [AnyObject]) {
            title = aTitle
            children = aChildren
        }
        
        func getDoc() -> String {
            return doc
        }

        func getTitle() -> String {
            return title
        }
        
        func getChildren() -> [AnyObject] {
            return children
        }
        
    }
    
    var menuitems = [MenuItem]()
    var menuTitle = ""
    var submenuitems = [MenuItem]()

    override func viewDidLoad() {
        super.viewDidLoad()

        let defaults = NSUserDefaults.standardUserDefaults()
        
        var language = defaults.stringForKey("prayer_language")
        if language == nil {
            language = NSLocalizedString("default_locale", comment: "")
        }
        let menuFile = NSBundle.mainBundle().URLForResource("prayers/" + language! + "/menu", withExtension: "xml")
        parser = NSXMLParser(contentsOfURL: menuFile!)!
        parser.delegate = self
        parser.parse()
    }
    
    func parser(parser: NSXMLParser, didStartElement elementName: String, namespaceURI: String?, qualifiedName qName: String?, attributes attributeDict: [String : String]) {
        if elementName == "menuitem" {
            if(menuTitle == "") {
                menuitems.append(MenuItem(aTitle: attributeDict["title"]!, aDoc: attributeDict["doc"]!))
            } else {
                submenuitems.append(MenuItem(aTitle: attributeDict["title"]!, aDoc: attributeDict["doc"]!))
            }
        } else if elementName == "menu" && attributeDict["title"] != nil {
            menuTitle = attributeDict["title"]!
        }
    }
    
    func parser(parser: NSXMLParser, didEndElement elementName: String, namespaceURI: String?, qualifiedName qName: String?) {
        if elementName == "menu" {
            menuitems.append(MenuItem(aTitle: menuTitle, aChildren: submenuitems))
            menuTitle = ""
        }

    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    // MARK: - Table view data source

    override func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        return 1
    }

    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return menuitems.count
    }

    
    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        guard let cell = tableView.dequeueReusableCellWithIdentifier("MenuTableViewCell", forIndexPath: indexPath) as? MenuTableViewCell else { fatalError() }
        cell.label.text = menuitems[indexPath.row].getTitle()
        return cell
    }
    
    override func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        let menuitem = menuitems[indexPath.row]
        if menuitem.getDoc() == "" {
            menuitems = (menuitem.getChildren() as? [MenuItem])!
            tableView.reloadData()
        } else {
            navigationController?.popViewControllerAnimated(true)
            let nav  = UIApplication.sharedApplication().keyWindow?.rootViewController as! UINavigationController
            let view = nav.viewControllers[0] as! ViewController
            print(menuitem.getDoc().stringByReplacingOccurrencesOfString(".html", withString: ""))
            view.loadPage(menuitem.getDoc().stringByReplacingOccurrencesOfString(".html", withString: ""))
        }
    }
    
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
