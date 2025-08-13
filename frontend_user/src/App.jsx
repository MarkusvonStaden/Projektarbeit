import { useEffect, useState, useCallback } from "react";
import {
  Sidebar,
  SidebarBody,
  SidebarItem,
  SidebarSection,
  SidebarHeading,
  SidebarLabel,
} from "@/components/sidebar";
import { SidebarLayout } from "@/components/sidebar-layout";
import { SidebarHeader } from "./components/sidebar";
import {

QuestionMarkCircleIcon,

PlusIcon,

InformationCircleIcon,

} from "@heroicons/react/20/solid";
import { Route, Routes } from "react-router-dom";
import { NewQuestion } from "@/components/new-question";
import { UserView, AdminView } from "@/components/views"

function Example() {
  const [userQuestions, setUserQuestions] = useState([]);
  const [adminQuestions, setAdminQuestions] = useState([]);
  const [activeItemId, setActiveItemId] = useState(null);

  const fetchQuestions = useCallback(async () => {
    try {
      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
      const userResponse = await fetch(`${backendUrl}/questions`);
      const data = await userResponse.json();
      const withoutAnswer = data.filter((item) => !item.answer);
      console.log("Fetched questions:", data);
      console.log("Filtered unanswered questions:", withoutAnswer);
      setUserQuestions(data);
      setAdminQuestions(withoutAnswer);
    } catch (error) {
      console.error("Failed to fetch questions:", error);
    }
  }, []);

  useEffect(() => {
    fetchQuestions();
  }, [fetchQuestions]);

  const handleItemClick = (id) => {
    setActiveItemId(id);
  };

  return (
    <SidebarLayout
      sidebar={
        <Sidebar>
          <SidebarHeader>
            <SidebarSection>
              <SidebarItem to="/">
                <PlusIcon />
                <SidebarLabel>New Question</SidebarLabel>
              </SidebarItem>
            </SidebarSection>
          </SidebarHeader>
          <SidebarBody>
            <SidebarSection>
              <SidebarHeading>User</SidebarHeading>
              {userQuestions.map((item) => (
                <SidebarItem
                  key={item.id}
                  to={`/user/${item.id}`}
                  onClick={() => handleItemClick(item.id)}
                  current={activeItemId === item.id ? "page" : undefined}
                >
                  <QuestionMarkCircleIcon />
                  <SidebarLabel>{item.question}</SidebarLabel>
                </SidebarItem>
              ))}
            </SidebarSection>
            <SidebarSection>
              <SidebarHeading>Admin</SidebarHeading>
              {adminQuestions.map((item) => (
                <SidebarItem
                  key={item.id}
                  to={`/admin/${item.id}`}
                  onClick={() => handleItemClick(item.id)}
                  current={activeItemId === item.id ? "page" : undefined}
                >
                  <InformationCircleIcon className="size-8" />
                  <SidebarLabel>{item.question}</SidebarLabel>
                </SidebarItem>
              ))}
            </SidebarSection>
          </SidebarBody>
        </Sidebar>
      }
    >
        <Routes>
          <Route path="/" element={<NewQuestion updateSidebar={fetchQuestions} />} />
          <Route path="/user/:id" element={<UserView updateSidebar={fetchQuestions} />} />
          <Route path="/admin/:id" element={<AdminView updateSidebar={fetchQuestions} />} />
        </Routes>
    </SidebarLayout>
  );
}

export default Example;