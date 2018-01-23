import java.util.ArrayList;

public class SingleNode {

// Instance variables
    private Object item;
    private SingleNode link;

// Constructors
    public SingleNode(Object item){
        this.item = item;
        this.link = null;
    }


// Instance Functions

    /**
     * Function to add a tail node or a linked list of nodes to
     * the current node.
     * @param guest
     * @return
     */
    public boolean addNode(SingleNode guest){
        if(this.link == null && guest.link == null){
            this.link = guest;
            return true;
        }else if (this.link == null){
            this.link = guest;
            if(guest.addNode(null))
                return true;
            return false;

        }else{
            if(guest.addNode(this.link)){
                this.link = guest;
                return true;
            }
            return false;
        } } // Close add node function

    /**
     * Removes the current node from a list
     */
    public void removeNode(){

    }


} // Close SingleNode Class
