//
//  MenuItemTableViewController.swift
//  Pauline Prayer Book
//
//  Created by Eremita on 25/04/17.
//
//

import UIKit

class MenuItemTableViewController: UITableViewController, XMLParserDelegate, UINavigationBarDelegate {
    
    var parser = XMLParser()
    
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
    var currentMenuitems = [MenuItem]()

    override func viewDidLoad() {
        super.viewDidLoad()
        //self.navigationController?.navigationBar.delegate = self
        
        let defaults = UserDefaults.standard //UserDefaults()
        
        var language = defaults.string(forKey:"prayer_language")
        if language == nil {
            language = NSLocalizedString("default_locale", comment: "")
        }
        let menuFile = Bundle.main.url(forResource:"prayers/" + language! + "/menu", withExtension: "xml")
        parser = XMLParser(contentsOf: menuFile!)!
        parser.delegate = self
        parser.parse()
        
        currentMenuitems = menuitems
    }
    
    func parser(_ parser: XMLParser, didStartElement elementName: String, namespaceURI: String?, qualifiedName qName: String?, attributes attributeDict: [String : String]) {
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
    
    func parser(_ parser: XMLParser, didEndElement elementName: String, namespaceURI: String?, qualifiedName qName: String?) {
        if elementName == "menu" {
            menuitems.append(MenuItem(aTitle: menuTitle, aChildren: submenuitems))
            menuTitle = ""
            submenuitems = [MenuItem]()
        }

    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    // MARK: - Table view data source

    override func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return currentMenuitems.count
    }

    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        guard let cell = tableView.dequeueReusableCell(withIdentifier: "MenuTableViewCell", for: indexPath as IndexPath) as? MenuTableViewCell else { fatalError() }
        cell.label.text = currentMenuitems[indexPath.row].getTitle()
        return cell
    }
    
    override func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        let menuitem = currentMenuitems[indexPath.row]
        if menuitem.getDoc() == "" {
            currentMenuitems = (menuitem.getChildren() as? [MenuItem])!
            tableView.reloadData()
        } else {
            navigationController?.popViewController(animated: true)
            let nav  = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
            let view = nav.viewControllers[0] as! ViewController
            view.loadPage(page: menuitem.getDoc().replacingOccurrences(of:".html", with: ""))
        }
    }
    /*
    func navigationBar(navigationBar: UINavigationBar, shouldPopItem item: UINavigationItem) -> Bool {
        let result = zip(currentMenuitems, menuitems).enumerate().filter() {
            $1.0 === $1.1
            }.map{$0.0}
        if(result.count == menuitems.count) {
            return true
        } else {
            currentMenuitems = menuitems
            tableView.reloadData()
            return false
        }
    }
    
    override func didMoveToParentViewController(parent: UIViewController?) {
        print("moved")
        //navigationController?.popViewControllerAnimated(true)
    }
    
    override func viewDidDisappear(animated: Bool) {
        print("disapear")
    }
    
    override func viewWillDisappear(animated : Bool) {
        // this is not yet working
        super.viewWillDisappear(animated)
        if (self.isMovingFromParentViewController()){
            print("moving")
        }
    }
    */
    
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
