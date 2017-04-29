//
//  menuViewController.swift
//  Pauline Prayer Book
//
//  Created by Eremita on 27/04/17.
//
//

import UIKit

class MenuViewController: UIViewController, UIPickerViewDelegate, UIPickerViewDataSource {

    @IBOutlet weak var prayerLanguage: UIPickerView!
    var languageData: [String] = [String]()
    var languageValues: [String] = [String]()
    
    @IBOutlet weak var fontSize: UIPickerView!
    var fontSizeData: [String] = [String]()
    var fontSizeValue: [String] = [String]()
    
    var languageChange = false
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let defaults = NSUserDefaults.standardUserDefaults()
        
        // Connect data:
        self.prayerLanguage.delegate = self
        self.prayerLanguage.dataSource = self
        
        self.fontSize.delegate = self
        self.fontSize.dataSource = self
        
        // Do any additional setup after loading the view.
        languageData = [NSLocalizedString("English", comment: ""),
                        NSLocalizedString("Polish", comment: ""),
                        NSLocalizedString("Latin", comment: ""),
                        NSLocalizedString("Italian", comment: ""),
                        NSLocalizedString("German", comment: ""),
                        NSLocalizedString("Croation", comment: "")]
        languageValues = ["en", "pl", "la", "it", "de", "hr"]
        
        var language = defaults.stringForKey("prayer_language")
        if language == nil {
            language = NSLocalizedString("default_locale", comment: "")
        }
        
        let activeLanguage = languageValues.indexOf(language!)
        if activeLanguage != nil {
            self.prayerLanguage.selectRow(activeLanguage!, inComponent: 0, animated: false)
        }
        
        fontSizeData = [NSLocalizedString("Very Small", comment: ""),
                        NSLocalizedString("Small", comment: ""),
                        NSLocalizedString("Medium", comment: ""),
                        NSLocalizedString("Large", comment: ""),
                        NSLocalizedString("Very Large", comment: "")]
        fontSizeValue = ["8", "11", "14", "17", "20"]
 
        var fontSize = defaults.stringForKey("font_size")
        if fontSize == nil {
            fontSize = "14"
        }
        
        let activeFontSize = fontSizeValue.indexOf(fontSize!)
        if activeFontSize != nil {
            self.fontSize.selectRow(activeFontSize!, inComponent: 0, animated: false)
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    // The number of columns of data
    func numberOfComponentsInPickerView(pickerView: UIPickerView) -> Int {
        return 1
    }
    
    // The number of rows of data
    func pickerView(pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        if pickerView == self.prayerLanguage {
            return languageData.count
        } else {
            return fontSizeData.count
        }
        
    }
    
    // The data to return for the row and component (column) that's being passed in
    func pickerView(pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        if pickerView == self.prayerLanguage {
            return languageData[row]
        } else {
            return fontSizeData[row]
        }
    }
    
    // Catpure the picker view selection
    func pickerView(pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
        // This method is triggered whenever the user makes a change to the picker selection.
        // The parameter named row and component represents what was selected.
        let defaults = NSUserDefaults.standardUserDefaults()

        if pickerView == self.prayerLanguage {
            defaults.setObject(languageValues[row], forKey: "prayer_language")
            self.languageChange = true
        } else {
            defaults.setObject(fontSizeValue[row], forKey: "font_size")
        }
    }
    

    
    // MARK: - Navigation

    override func willMoveToParentViewController(parent: UIViewController?) {
        super.willMoveToParentViewController(parent)
        if parent == nil && self.languageChange {
            let nav  = UIApplication.sharedApplication().keyWindow?.rootViewController as! UINavigationController
            let view = nav.viewControllers[0] as! ViewController
            view.languageChanged()
        }
    }
    
    @IBAction func about(sender: UIButton) {
        navigationController?.popViewControllerAnimated(true)
        let nav  = UIApplication.sharedApplication().keyWindow?.rootViewController as! UINavigationController
        let view = nav.viewControllers[0] as! ViewController
        view.loadPage("about")
        
    }

}
