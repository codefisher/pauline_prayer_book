//
//  XMLMenuReader.swift
//  Pauline Prayer Book
//
//  Created by Michael Buckley on 22/3/20.
//  Copyright © 2020 Michael Buckley. All rights reserved.
//

import Foundation

class MenuItem {
    var title: String = ""
    var doc: String = ""
    var children: [MenuItem]
    
    init(aTitle: String, aDoc: String) {
        title = aTitle
        doc = aDoc
        children = [MenuItem]()
    }
    
    init(aTitle: String) {
        title = aTitle
        doc = ""
        children = [MenuItem]()
    }
    
    func getDoc() -> String {
        return doc
    }

    func getTitle() -> String {
        return title
    }
    
    func getChildren() -> [MenuItem] {
        return children
    }
    
    func setChildren(aChildren: [MenuItem]) {
        children = aChildren
    }
    
}

class XMLMenuReader: NSObject, XMLParserDelegate {
    
    var parser: XMLParser
    
    /*    var menuitems = [MenuItem]()
    var menuTitle = ""
    var submenuitems = [MenuItem]()
    var currentMenuitems = [MenuItem]()
     */
    
    var menuItems: [MenuItem] = [MenuItem]()
    var stack: [[MenuItem]] = [[MenuItem]]()
    
    override init() {
        let defaults = UserDefaults.standard //UserDefaults()
        
        var language = defaults.string(forKey:"prayer_language")
        if language == nil {
            language = NSLocalizedString("default_locale", comment: "")
        }
        let menuFile = Bundle.main.url(forResource:"prayers/" + language! + "/menu", withExtension: "xml")
        parser = XMLParser(contentsOf: menuFile!)!
        
        super.init()
        
        parser.delegate = self
        parser.parse()
    }
    
    func getItems() -> [MenuItem] {
        return self.menuItems
    }
    
    func parser(_ parser: XMLParser, didStartElement elementName: String, namespaceURI: String?, qualifiedName qName: String?, attributes attributeDict: [String : String]) {
        if elementName == "menuitem" {
            menuItems.append(MenuItem(aTitle: attributeDict["title"]!, aDoc: attributeDict["doc"]!))
        } else if elementName == "menu" && attributeDict["title"] != nil {
            menuItems.append(MenuItem(aTitle: attributeDict["title"]!))
            stack.append(menuItems)
            menuItems = [MenuItem]()
        }
    }
    
    func parser(_ parser: XMLParser, didEndElement elementName: String, namespaceURI: String?, qualifiedName qName: String?) {
        if elementName == "menu" && stack.count != 0 {
            let levelUp = stack.popLast()
            levelUp?.last?.setChildren(aChildren: menuItems)
            menuItems = levelUp!
        }
    }
    
}
