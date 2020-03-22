//
//  MenuItemTableViewController.swift
//  Pauline Prayer Book
//
//  Created by Eremita on 25/04/17.
//
//

import UIKit

class MenuItemTableViewController: UITableViewController  {
    
    var menu: XMLMenuReader? = nil
    var currentMenuitems = [MenuItem]()
    var history = [AnyObject]()
    

    override func viewDidLoad() {
        super.viewDidLoad()
        menu = XMLMenuReader()
        currentMenuitems = (menu?.getItems())!
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
            history.append(currentMenuitems as AnyObject)
            currentMenuitems = menuitem.getChildren()
            tableView.reloadData()
        } else {
            navigationController?.popViewController(animated: true)
            let view = self.navigationController!.viewControllers[0] as! ViewController
            view.loadPage(page: menuitem.getDoc().replacingOccurrences(of:".html", with: ""))
            #if targetEnvironment(macCatalyst)
            self.view.removeFromSuperview()
            #endif
        }
    }

}
